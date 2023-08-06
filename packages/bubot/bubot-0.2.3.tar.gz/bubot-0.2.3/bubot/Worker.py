import multiprocessing
import asyncio
import time
import json
from bubot.BujectError import BujectError
from bubot import BubotConfig
from bubot.Buject import Buject


class Worker(multiprocessing.Process, Buject):
    def __init__(self, worker_id, **kwargs):
        Buject.__init__(self, **kwargs)
        multiprocessing.Process.__init__(self)
        self.type = 'worker'
        self.id = worker_id
        self.buject = {}
        self.subscribe_list = {}
        config = BubotConfig.config_to_simple_dict(BubotConfig.load_config('Worker'))
        self.config = BubotConfig.update_dict(config, self.config)
        pass

    # def on_close(self):
    #     if self.loop:
    #         self.loop.close()
    #     if self.redis:
    #         self.redis.close()
    #     Buject.on_close(self)

    def run(self):
        # self.log("Start worker {name}".format(name=self.name))
        self.loop = asyncio.get_event_loop()
        self.init()
        self.loop.run_until_complete(self.handler())
        self.on_close()

    async def on_init(self):
        await super().on_init()
        for elem in self.config['buject']:
            await self.run_buject(elem, self.config['buject'][elem])

    # async def on_run(self):
    #     await asyncio.sleep(5)
        # print(self.get_name())

    async def run_buject(self, buject_id, config):
        try:
            buject_class = BubotConfig.get_class(
                'buject.{buject}.{buject}.{buject}'.format(buject=config['param']['buject']))
            buject_class = buject_class(id=buject_id, config=config, bubot=self.bubot, loop=self.loop)
            self.buject[buject_id] = {
                'class': buject_class,
                'task': self.loop.create_task(buject_class.handler())
            }
        except Exception as e:
            await self.error("worker.add_buject({0}):{1}".format(buject_id, str(e)))

    #
    # async def request_stop_buject(self, message):
    #     del self.buject[message['param']]
    #
    async def request_run_buject(self, message):
        await self.run_buject(message['param']['id'], message['param']['config'])

    # def __str__(self):
    #     return self.id

    # async def check_close(self):
    #     if not self.buject or self.param['buject_status'] == 'close':  # выключаем если ничего не выполняется
    #         self.param['buject_status'] = ''
    #         await self.send_buject_param()
    #         return True
    #     return False


class WorkerQueue(Worker):
    def __init__(self, worker_id, queue, **kwargs):
        super().__init__(worker_id, **kwargs)
        self.id = '{0}_{1}'.format(queue, worker_id)
        self.queue = queue
        self.type = 'queue'
        self.buject = None

    async def handler(self):
        await self.get_broker()
        await self.broker.handler_queue()
