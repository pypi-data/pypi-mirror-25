import uuid
from bson import json_util
import asyncio
from bubot.BujectError import BujectError
from bubot.Action import Action
from bubot import BubotConfig
import asyncio_redis


class BrokerClientRedis():
    def __init__(self):
        self.redis = None
        self.lock = None
        self.awaiting_request = {}

    async def check_redis(self, **kwargs):
        res = Action("Buject.check_redis")
        with await self.lock_redis:
            if self.redis:
                return res.set_end()
            host = self.bubot.get('redis_host', 'localhost')
            port = self.bubot.get('redis_port', 6379)
            db = self.bubot.get('redis_db', 0)
            timeout = self.bubot.get('redis_timeout', 20)
            pool_size = self.param.get('redis_pool_size', 3)
            try:
                self.redis = await asyncio.wait_for(
                    asyncio_redis.Pool.create(host=host, port=port, db=db, poolsize=pool_size, **kwargs), timeout)
                return res.set_end()
            except asyncio.futures.TimeoutError:
                raise TimeoutError('Buject.check_redis({0}:{1}))'.format(host, port), action=res)
            except Exception as e:
                raise BujectError(str(e), 'Buject.check_redis()', action=res)

    async def handle_get_redis_msg(self):
        await self.check_redis()
        self.subscribe_list = await self.get_subscribe_list()
        if not await self.subscribe():
            return False
        while True:
            msg_redis = await self.pubsub.next_published()
            if msg_redis:
                try:
                    message = json_util.loads(msg_redis.value)
                    method = message['method']
                    message_type = message['type']
                    receiver = message['receiver']
                    if method == 'close' and self.type in receiver and receiver[self.type] == self.id:
                        self.param['buject_status'] = 'close'
                        break
                    try:
                        if message_type == 'request':
                            result = await self.process_request(message)
                        elif message_type == 'response':
                            result = await self.process_response(message)
                        else:
                            msg = '{0}.process_message({1}) error: unknown message type {2} '.format(self.id, method,
                                                                                                     message_type)
                            await self.error(msg)
                            result = {'type': 'error', 'data': msg}

                    except BujectError as e:
                        result = {'type': 'error', 'data': e.json()}
                    except Exception as e:
                        msg = '{0}.process_message({1}) error: {2}'.format(self.id, method, e)
                        await self.error(msg)
                        result = {'type': 'error', 'data': msg}
                    finally:
                        need_response = message.get('response', False)
                        if message_type == 'request' and need_response:
                            await self.send_response(message, result)
                except Exception as e:
                    await self.error('{0}.bad format redis msg: {1}'.format(self.id, e))
        return True

    async def process_request(self, message):
        method = 'request_{0}'.format(message['method'])
        return await getattr(self, method)(message)

    async def process_response(self, message):
        if message['uuid'] in self.waiting_response:
            future = self.waiting_response.get(message['uuid'], False)
            if future:
                future['future'].set_result(message['data'])
                return True
        return False

    async def subscribe(self, subscribe_list=None):
        if not subscribe_list:
            if not self.subscribe_list:
                return False
            subscribe_list = self.subscribe_list
        await self.check_redis()
        with (await self.lock_redis):
            if not self.pubsub:
                self.pubsub = await asyncio.wait_for(self.redis.start_subscribe(), 1)
            subscribe = []
            for element in subscribe_list:
                subscribe.append(element)
            # await asyncio.wait_for(self.pubsub.subscribe(subscribe), 1)
            await self.pubsub.subscribe(subscribe)
        return True
    pass

    async def unsubscribe(self, subscribe_list):
        if not subscribe_list:
            return False
        subscribe = []
        for element in subscribe_list:
            subscribe.append(element)
        await self.pubsub.request_unsubscribe(subscribe)
        return True

    async def send_sync_request(self, request=None, **kwargs):
        message = await self.send_request2(request, **kwargs)
        self.waiting_response[message["uuid"]] = {
            'future': asyncio.Future(),
            'request': request,
            'receiver_buject': message['receiver']['id'],
            'time_start': time.time()
        }

        try:
            result = await asyncio.wait_for(
                self.waiting_response[message["uuid"]]["future"], message.get('timeout', 120))
        finally:
            del self.waiting_response[message["uuid"]]
        return result

    async def send_async_request(self, request=None, **kwargs):
        message = await self.send_request2(request, **kwargs)
        self.waiting_response[message["uuid"]] = {
            'future': asyncio.Future(),
            'request': request,
            'receiver_buject': message['receiver']['id'],
            'time_start': time.time()
        }
        return message


    async def send_request(self, request=None, **kwargs):

        # param = {}
        receiver_method = kwargs.get('request', request)
        receiver_buject = kwargs.get('receiver', 'bubot')
        receiver_type = kwargs.get('receiver_type', 'buject')
        queue = kwargs.get('queue', None)

        await self.debug('Buject "{0}" send request {1}'.format(self.id, request))
        receiver_channel = '{0}:{1}'.format(receiver_type, receiver_buject)

        message = {
            "sender": {"type": self.type, "id": self.id},
            "receiver": {"type": receiver_type, "id": receiver_buject},
            "type": "request",
            "method": receiver_method,
            "data": kwargs.get("data", {}),
            "response": kwargs.get("response", False),
            "uuid": str(uuid.uuid4())
        }

        if queue:
            await self.add_to_queue(queue, message)
        else:
            await self.send_message(receiver_channel, message)

        if message['response']:
            self.waiting_response[message["uuid"]] = {
                'future': asyncio.Future(),
                'request': request,
                'receiver_buject': receiver_buject,
                'time_start': time.time()
            }

            try:
                result = await asyncio.wait_for(
                    self.waiting_response[message["uuid"]]["future"], message.get('timeout', 120))
            finally:
                del self.waiting_response[message["uuid"]]
            return result
        return None

    async def send_response(self, message_data, response_data):

        message = {
            "receiver": message_data['sender'],
            "sender": message_data['receiver'],
            "type": "response",
            "method": message_data['method'],
            "data": response_data,
            "uuid": message_data['uuid']
        }
        channel = '{0}:{1}'.format(message['receiver']['type'], message['receiver']['id'])

        await self.send_message(channel, message)

    async def add_to_queue(self, queue_name, message, debug_info=None):
        await self.redis.lpush("queue_{0}".format(queue_name),
                               [json_util.dumps(message), ])
        if self.param['log'] > 0:
            if self.param['log'] > 2:
                self.log('Buject "{0}" add_to_queue: {1} message:{2}'.format(self.id, queue_name, message))
            elif self.param['log'] > 1:
                self.log(
                    'Buject "{0}" send message: {1}'.format(self.id, debug_info if debug_info else queue_name))

    async def send_message(self, channel, message, debug_info=None):
        # if self.redis:
        await self.redis.publish(channel, json_util.dumps(message, ensure_ascii=False))
        if self.param['log'] > 0 and message['method'] != 'console':
            if self.param['log'] > 2:
                self.log('Buject "{0}" send message: {1} message:{2}'.format(self.id, channel, message))
            elif self.param['log'] > 1:
                self.log(
                    'Buject "{0}" send message: {1}'.format(self.id, debug_info if debug_info else channel))

    async def wait_async_response(self, messages):
        tasks = []
        for message in messages:
            tasks.append(self.waiting_response[message["uuid"]]["future"])

        result = await asyncio.wait(tasks)

        for message in messages:
            del self.waiting_response[message["uuid"]]

        return result


    async def send_request2(self, request=None, **kwargs):

        # param = {}
        receiver_method = kwargs.get('request', request)
        receiver_buject = kwargs.get('receiver', 'bubot')
        receiver_type = kwargs.get('receiver_type', 'buject')
        queue = kwargs.get('queue', None)

        await self.debug('Buject "{0}" send request {1}'.format(self.id, request))
        receiver_channel = '{0}:{1}'.format(receiver_type, receiver_buject)

        message = {
            "sender": {"type": self.type, "id": self.id},
            "receiver": {"type": receiver_type, "id": receiver_buject},
            "type": "request",
            "method": receiver_method,
            "data": kwargs.get("data", {}),
            "response": kwargs.get("response", False),
            "uuid": str(uuid.uuid4())
        }

        if queue:
            await self.add_to_queue(queue, message)
        else:
            await self.send_message(receiver_channel, message)

        return message

        # try:
        #     result = await asyncio.wait_for(
        #         self.waiting_response[message["uuid"]]["future"], message.get('timeout', 120))
        # finally:
        #     del self.waiting_response[message["uuid"]]
        # return result


class BubotMsg:
    def __init__(self):
        self.sender = None
        self.channel = None
        self.topic = None
        self.data = None
        self.uuid = None
        pass

    def init(self, data):
        self.sender = data.get('sender', None)
        self.channel = data.get('channel', 'bubot')
        self.topic = data.get('topic', 'console')
        self.data = data.get('data', None)
        self.uuid = data.get('uuid', uuid.uuid4())

    def get_queue_broker(self, broker, broker_param):
        pass

    def get_publish_broker(self, broker, broker_param):
        pass

    def add_to_queue(self, queue, broker):
        pass

    def publish(self, broker):
        pass

    def handle_publish_msg(self, worker):
        pass

    def dump(self):
        return json_util.dumps([self.topic, self.data, self.sender, self.uuid], ensure_ascii=False)
