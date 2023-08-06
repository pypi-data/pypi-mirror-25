import uuid

from bson import json_util


class BrokerClient:
    def __init__(self, buject):
        self.buject = buject
        self.class_msg = BrokerMsg

    async def initialize(self):
        pass

    async def get_subscribe_list(self):
        subscribe_list = {'{0}:{1}'.format(self.buject.type, self.buject.id): {}}

        if 'incoming_event' in self.buject.config:
            for method_name in self.buject.config['incoming_event']:
                method_param = self.buject.config['incoming_event'][method_name]
                method = 'incoming_event_{0}'.format(method_name)
                if hasattr(self, method):
                    if 'buject' not in method_param:
                        method_param['buject'] = self.buject.bubot['name']
                    if 'name' not in method_param:
                        method_param['name'] = method_name
                    if 'type' not in method_param:
                        method_param['type'] = 'buject'
                    ch = '{0}:{1}:event:{2}'.format(method_param['type'],
                                                    method_param['buject'],
                                                    method_param['name'])
                    subscribe_list[ch] = {'buject': self.buject.id, 'method': method,
                                          'param': self.buject.config['incoming_event'][method_name]}
                else:
                    await self.buject.log(
                        "get_subscribe_list({0}) method is not defined: {1}".format(self.buject.get_param('name'),
                                                                                    method))
        # if 'outgoing_request' in self.config:
        #     for method_name in self.config['outgoing_request']:
        #         method_param = self.config['outgoing_request'][method_name]
        #         if 'response' in method_param and method_param['response']:
        #             method = 'incoming_response_{0}'.format(method_param['response'])
        #             if hasattr(self, method):
        #                 ch = '{0}:{1}:response:{2}'.format(self.type, self.id, method_param['response'])
        #                 subscribe_list[ch] = {'buject': self.id,
        #                                       'method': method,
        #                                       'param': self.config['outgoing_request'][method_name]}
        #             else:
        #                 await self.log("{0} method is not defined: {1}".format(self.param['name'], method))
        # if 'incoming_request' in self.config:
        #     for method_name in self.config['incoming_request']:
        #         # method_param = self.config['incoming_request'][method_name]
        #         method = 'incoming_request_{0}'.format(method_name)
        #         if hasattr(self, method):
        #             ch = '{0}:{1}:request:{2}'.format(self.type, self.id, method_name)
        #             subscribe_list[ch] = {'buject': self.id, 'method': method,
        #                                   'param': self.config['incoming_request'][method_name]}
        #         else:
        #             await self.log("{0} method is not defined: {1}".format(self.param['name'], method))
        return subscribe_list

        # async def initialize(self):
        #     pass
        # res = Action('BubotClient.initialize')
        # try:
        #     self.redis = await asyncio.wait_for(
        #         asyncio_redis.Connection.create(host=self.host, port=self.port, db=self.db), self.timeout)
        #     return res
        # except asyncio.futures.TimeoutError:
        #     raise TimeoutError('Redis.Connection({0}:{1}))'.format(self.host, self.port, self.db))
        # except Exception as e:
        #     raise BujectError(e, action=res)

    # async def subscribe(self, channel):
    #     if not self.subscriber:
    #         self.subscriber = await asyncio.wait_for(self.redis.start_subscribe(), self.timeout)
    #     await asyncio.wait_for(self.subscriber.request_subscribe(channel), self.timeout)
    #
    # async def publish(self, channel, message):
    #     await self.redis.publish(channel, message)
    #
    # async def next_published(self):
    #     return await self.subscriber.next_published()
    #
    # async def hset(self, key, field, value):
    #     return await self.redis.hset(key, field, value)

    def get_buject_for_worker(self, worker_id):
        res = {}
        for buject_id in self.buject.config['buject']:
            try:
                if self.buject.config['buject'][buject_id]['param']['worker_id'] == worker_id:
                    res[buject_id] = self.buject.config['buject'][buject_id]
            finally:
                pass
        return res

    def get_worker_param(self, worker_id):

        return {'buject': self.get_buject_for_worker(worker_id)}


class CloseBrokerClient(Exception):
    pass


class BrokerMsg:
    def __init__(self):
        self.sender = None
        self.receiver = None
        self.topic = None
        self.data = None
        self.uuid = None
        self.type = None  # msg, request, response, error
        pass

    def init(self, data):
        self.sender = data.get('sender', None)
        self.receiver = data.get('receiver', 'bubot')
        self.type = data.get('type', 'msg')
        self.topic = data.get('topic', 'console')
        self.data = data.get('data', None)
        self.uuid = data.get('uuid', uuid.uuid4())
        return self

    def __str__(self):
        return 'sender: {0}, receiver: {1}, topic:{2}'.format(self.sender, self.receiver, self.topic)

    async def handler_msg(self):
        return None

    async def get_buject_config(self, buject_id):
        pass

    def init_from_json(self, json_data):
        return self.init(json_util.loads(json_data))

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
        return json_util.dumps({
            'sender': self.sender,
            'receiver': self.receiver,
            'type': self.type,
            'topic': self.topic,
            'data': self.data,
            'uuid': self.uuid
        }, ensure_ascii=False)
