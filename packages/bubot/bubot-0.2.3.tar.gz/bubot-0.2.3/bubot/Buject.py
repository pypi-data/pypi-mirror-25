from bubot.BubotDb import BubotDb
from bubot.BujectError import BujectError, UserError
from bubot.Action import Action
from bubot import BubotConfig
import time
import json
import asyncio
import asyncio_redis
import uuid
from bson import json_util


class Buject:
    DEBUG = 2
    INFO = 1

    def __init__(self, **kwargs):
        self.bubot = kwargs.get('bubot', {})
        self.config = kwargs.get('config', {'param': {}})
        # self.worker = kwargs.get('worker', None)
        # self.redis = None
        # self.pubsub = None
        self.broker = None
        self.loop = kwargs.get('loop', None)
        self.db = kwargs.get('db', None)
        self.param = {}
        # self.fps = 0
        # self.fps_time = time.time()
        # self.time = time.time()
        self.subscribe_list = {}
        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.type = 'buject'
        # self.lock_redis = None
        # self.waiting_response = {}
        # self.path = None

    def init(self):
        self.id = self.get_param('id', self.id)
        # if self.config:
        #     self.param = BubotConfig.config_to_simple_dict(self.config['param'])
        return self

    def get_name(self):
        return '{0}_{1}'.format(self.type, self.id)

    async def handler(self):
        await self.get_broker()
        await asyncio.gather(self.broker.handler_msg(), self.main())

    async def handler_msg(self, msg):
        return await getattr(self, 'action_{0}'.format(msg.topic))(msg.data)

    async def handler_request(self, msg):
        return await self.handler_msg(msg)

    async def handler_response(self, msg):
        return await self.handler_msg(msg)

    async def get_broker(self):
        res = Action('get_broker')
        broker_name = self.bubot.get('broker_name', '')

        try:
            broker_class = BubotConfig.get_class('bubot.BrokerClient{0}.BrokerClient{0}'.format(broker_name))
        except Exception as e:
            raise UserError('Broker not import', '{0}: {1}'.format(broker_name, str(e)))
        self.broker = broker_class(self)
        res.add_stat(await self.broker.initialize())
        return res.set_end()

    async def main(self):
        while True:
            try:
                if not self.get_param('buject_status'):
                    self.set_param('buject_status', 'init')
                method = 'on_{0}'.format(self.get_param('buject_status'))
                await getattr(self, method)()
            except CloseMain:
                break
            except CloseBuject:
                break
            except BujectError as e:
                self.set_param('buject_status', 'error')
                self.set_param('buject_status_detail', e.to_json())
                pass
            except Exception as e:
                self.set_param('buject_status', 'error')
                self.set_param('buject_status_detail', BujectError(str(e)).to_json())
                pass
        pass

    def get_param(self, name, default=None):
        group = 'param'
        try:
            _group = self.config[group]
            try:
                return _group.get(name, default)
                # return _group[name]['value']
            except KeyError:
                raise KeyError('{0} get_param({1} {2} - Key value not found)'.format(self.__class__.__name__, group, name))
        except KeyError:
            raise KeyError('{0} get_param({1} {2}) - group not found'.format(self.__class__.__name__, group, name))

    def set_param(self, name, value, group='param'):
        try:
            self.config[group][name] = value
        except KeyError:
            raise KeyError('{0} set({1}, {2}) - group not found'.format(self.__class__.__name__, group, name))

    def get_db(self):
        if not self.db:
            self.db = BubotDb.connect()

        if not self.db:
            raise BujectError('Нет подключения к БД')
        return self.db

    async def request_subscribe(self, message):
        return await self.broker.subscribe(message['data'])

    async def request_unsubscribe(self, message):
        await self.broker.unsubscribe(message['data'])

    # async def calc_fps(self):
    #     # счетчик FPS
    #     fps_time_delta = self.time - self.fps_time
    #     self.fps += 1
    #
    #     if fps_time_delta > 1:
    #         if self.fps == 1:  # выполняется реже одного раза в секунду, пишем сколько секунда надо для одного раза
    #             self.param['buject_fps'] = round(fps_time_delta) * -1
    #         else:
    #             self.param['buject_fps'] = self.fps
    #         self.fps_time = self.time
    #         self.fps = 0
    #     # расчитываем время сна исходя из ограничений max_fps
    #     sleep_time = 0
    #     elapsed_time = time.time() - self.fps_time
    #     if self.param['buject_max_fps'] > 0:  # несклько раз в секунду
    #         time_left = 1 - elapsed_time
    #         if self.fps < self.param['buject_max_fps']:
    #             sleep_time = round(time_left / (self.param['buject_max_fps'] - self.fps), 3)
    #         else:
    #             sleep_time = time_left
    #     elif self.param['buject_max_fps'] < 0:
    #         sleep_time = self.param['buject_max_fps'] * -1 - elapsed_time
    #
    #     # авто обновление параметров
    #     if self.time - self.param['buject_update'] > self.param['buject_auto_update']:
    #         self.param['buject_update'] = self.time
    #         await self.send_buject_param()
    #
    #     return sleep_time if sleep_time > 0 else 0

    # async def send_buject_param(self):
    #     try:
    #         await self.redis.hset('{0}:param'.format(self.type), self.id,
    #                               json_util.dumps(self.param))
    #     except AttributeError:
    #         await self.error('{0} {1}.send_buject_param: redis not init'.format(self.type, self.id))

    async def on_init(self):
        self.set_param('buject_status', 'wait')
        # await self.calc_fps()
        # await self.send_buject_param()

    async def on_wait(self):
        self.set_param('buject_status', 'ready')
        # await self.calc_fps()
        # await self.send_buject_param()

    async def on_ready(self):
        self.set_param('buject_status', 'run')
        # await self.calc_fps()
        # await self.send_buject_param()

    async def on_run(self):
        raise CloseMain()
        # await asyncio.sleep(1)
        # print(self.get_name())
        # raise CloseMain('')
        # await self.calc_fps()
        pass

    async def on_close(self):
        self.set_param('buject_status', '')
        # await self.calc_fps()
        # await self.broker.send_buject_param()
        raise CloseBuject()

    async def on_error(self):
        await asyncio.sleep(5)
        # await self.calc_fps()
        pass

    async def incoming_event_system(self, message, debug_info=None):
        # data = json_util.loads(message['data'])
        # if 'buject' in data['param'] and data['param']['buject'] != self.param['name']:
        #     return
        # command = data['param']['command']
        # if command == 'terminate':
        #     self.status['terminate'] = True
        #     return
        # if command == 'update':
        #     config = json_util.loads(data['param']['config'])
        #     if self.param['buject'] == 'Bubot':  # это головной процесс
        #         self.read_config(config)
        #     else:
        #         if self.param['name'] not in config['depend_buject']:  # если в новом конфиге текущего модуля нет, то торможим его
        #             self.status['terminate'] = True
        #             return
        #         self.read_config(config['depend_buject'][self.param['name']])
        #     # self.subscribe()
        #     # self.wait_depend_buject()
        return

    async def request_close(self, message, debug_info=None):
        self.param['buject_status'] = ""
        await self.on_close()
        worker_id = self.param['worker_id']
        if worker_id:
            await self.broker.send_request("close_buject", self.id, receiver=worker_id, receiver_type="worker")
            await self.broker.send_request('unsubscribe', self.subscribe_list, receiver=worker_id, receiver_type='worker')
        return

    def get_value(self, param, config=None):
        try:
            config = config if config else self.config
            return config['param'][param]['value']
        except Exception:
            return ""

    # async def get_buject_config(self, buject_id):
    #     result = await self.redis.hget('buject:config', buject_id)
    #     return json_util.loads(result)
    #
    # async def get_buject_params(self, buject_id):
    #     result = await self.redis.hget('buject:param', buject_id)
    #     return json_util.loads(result)

    async def log(self, message):
        print(message)
        # self.send_request("console", {"time": time.time(), "message": message})

    async def debug(self, message):
        print(message)
        # self.send_request("console", {"time": time.time(), "message": message})

    async def error(self, message, data=None):
        # message = 'Error {0}:{1} - {2} ({3})'.format(self.bubot['name'],
        #                                              self.param['name'] if 'name' in self.param else "", text, data)
        print(message)
        # if self.redis:
        #     self.send_request("console", {"time": time.time(), "message": message})


class CloseMain(Exception):
    pass


class CloseBuject(Exception):
    pass
