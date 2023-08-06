import asyncio
import os

import aiohttp_jinja2
import jinja2
from aiohttp.web import Application, HTTPFound
from aiohttp_session import SimpleCookieStorage
from aiohttp_session import get_session, session_middleware

from bubot import BubotConfig
from bubot.Action import Action
from bubot.Buject import Buject, CloseBuject
from bubot.Ui import Ui
from bubot.Worker import Worker, WorkerQueue


class Bubot(Buject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config_path = ''
        self.app = None
        self.app_handler = None
        self.server = None
        # self.name = 'Bubot'
        # self.config_full = None
        self.type = 'bubot'
        self.worker = {}
        self.worker_config = {}

    def init(self):
        super().init()
        self.bubot = self.config['param']

    def run(self, file_name=None):
        self.loop = asyncio.get_event_loop()
        self.app = Application(loop=self.loop, middlewares=[session_middleware(SimpleCookieStorage()), authorize])
        self.app['bubot'] = self
        self.loop.run_until_complete(self.read_bubot_config(file_name))
        try:
            self.loop.run_until_complete(self.handler())
        except KeyboardInterrupt:
            pass
        finally:
            if self.app_handler:
                self.app_handler.close()
                self.loop.run_until_complete(self.app_handler.wait_closed())
                self.loop.run_until_complete(self.app_handler.shutdown(60.0))
            self.loop.run_until_complete(self.app.shutdown())
            self.loop.run_until_complete(self.app.cleanup())
        self.loop.close()
        #
        # # print("Read buject")
        # res.add_stat(await self.add_all_buject())
        # # print("Run worker")
        # res.add_stat(await self.start_all_worker())
        # return res.set_end()
        # pass

    async def read_bubot_config(self, file_name=None):
        self.config_path = file_name
        res = Action("Bubot.read_bubot_config")
        user_config = BubotConfig.read_config(file_name) if file_name else {}
        cache = {}
        self.config, cache = BubotConfig.update_config('bubot', 'Bubot', {}, user_config, cache)
        for elem in self.config['buject']:
            try:
                buject_name = self.config['buject'][elem]['param']['buject']['value']
            except KeyError:
                print('buject \'{0}\' - not defined base buject'.format(elem))
                continue
            self.config['buject'][elem], cache = BubotConfig.load_config('buject', cache, buject_name,
                                                                         self.config['buject'][elem])

        for elem in self.config['ui']:
            self.config['ui'][elem], cache = BubotConfig.load_config('ui', cache, elem, self.config['ui'][elem])
        # self.config['worker'], cache = BubotConfig.load_config('Worker')

        self.config = BubotConfig.config_to_simple_dict(self.config)
        self.init()
        res.set_end()
        return res

    async def on_init(self):
        await super().on_init()
        res = Action('Bubot.on_init')
        self.app['ui'] = res.add_stat(await self.import_ui_handlers())
        self.app_handler = self.app.make_handler()
        port = self.get_param('web_port')
        print("Run web server port {port}".format(port=port))
        self.server = await self.loop.create_server(self.app_handler, None, port)
        res.add_stat(await self.add_all_buject())
        res.add_stat(await self.start_all_worker())
        pass

    async def on_error(self):
        print(self.param['buject_status_detail'])
        raise CloseBuject(self.param['buject_status_detail'])

    async def import_ui_handlers(self):
        res = Action("WebServer.import_ui_handlers")
        try:
            ui = BubotConfig.get_available_ui()
            ui = BubotConfig.config_to_simple_dict(ui)
        except Exception as e:
            print('Error BubotConfig.get_available_ui(): ', str(e))
            return res.set_end(False)
        try:
            self.app.router.add_static("/static", "./static")
        except ValueError as e:
            print('No static resources: ', str(e))
        # self.app.router.add_route('*', "/login", Login, name='login')
        template_loaders = {}
        for elem in ui:
            try:
                if os.path.isfile('./ui/{0}/{0}.py'.format(elem)):
                    ui_view = BubotConfig.get_class('ui.{0}.{0}.{0}'.format(elem))
                else:
                    ui_view = Ui
                ui_base_url = '/ui/{0}'.format(elem)
                ui_view.add_route(self.app, elem, ui_view)
                template_loaders[elem] = jinja2.FileSystemLoader('.' + ui_base_url)
                # template_path.append('.' + ui_base_url)
            except Exception as e:
                # raise RuntimeError('import_ui_handlers({1}): {0}'.format(e, elem))
                print('Error import_ui_handlers({1}): {0}'.format(e, elem))

        aiohttp_jinja2.setup(self.app, loader=jinja2.PrefixLoader(template_loaders),
                             block_start_string='<%',
                             block_end_string='%>',
                             variable_start_string='%%',
                             variable_end_string='%%'
                             # comment_start_string='<#',
                             # comment_end_string='#>'
                             )
        return res.set_end(ui)

    async def start_all_worker(self):
        res = Action("Bubot.start_all_worker")
        count_worker = self.get_param('count_workers')
        if count_worker > 0:
            for i in range(count_worker):
                res.add_stat(self.add_worker(i + 1, self.worker_config))

        if self.config['queue']:
            for queue_id in self.config['queue']:
                for i in range(self.config['queue'][queue_id]):
                    res.add_stat(self.add_worker(i + 1, queue_id))

        return res.set_end()

    def add_worker(self, worker_id, queue=None):
        res = Action('Bubot.add_worker')
        worker_config = self.broker.get_worker_param(worker_id)
        worker = WorkerQueue(worker_id, queue, config=worker_config, bubot=self.bubot) \
            if queue else Worker(worker_id, config=worker_config, bubot=self.bubot)
        worker.start()
        self.worker[worker.id] = worker
        return res.set_end()

    # async def start_worker(self, worker_id, worker_config, queue_id=None):
    #     try:
    #         cl_worker = BubotConfig.get_class(
    #             'worker.{buject}.{buject}.{buject}'.format(buject=worker_config['param']['buject']['value']))
    #         worker = cl_worker(id=worker_id, bubot=self.param, config=worker_config, worker=worker_id)
    #         worker.start()
    #         # self.worker[worker_id] = worker
    #         return worker
    #     except BujectError as e:
    #         raise BujectError(e.msg, '{0} <= start_worker({1})'.format(e.detail, worker_id))
    #     except Exception as e:
    #         raise BujectError(str(e), 'start_worker({0})'.format(worker_id))

    async def add_all_buject(self):
        res = Action("Bubot.add_all_buject")
        for buject_id in self.config['buject']:
            res.add_stat(await self.add_buject(buject_id, self.config['buject'][buject_id]))
        return res.set_end()

    async def add_buject(self, buject_id, buject_config):
        res = Action("Bubot.add_buject")
        await self.broker.save_buject_config('buject_{0}'.format(buject_id), buject_config)
        return res.set_end()

    # async def run_buject(self, buject_id):
    #     res = Action("Bubot.run_buject")
    #     active_workers = await self.action_get_active_worker()
    #     buject_config = await self.get_buject_config(buject_id)
    #     worker_id = self.get_value('worker_id', buject_config)
    #     if worker_id:
    #         if worker_id and worker_id in active_workers:
    #             worker_param = json.loads(active_workers[worker_id])
    #             if worker_param['buject_status'] == 'run':
    #                 await self.send_request('add_buject', buject_id, receiver=worker_id, receiver_type='worker')
    #                 return res.set_end()
    #             else:
    #                 self.error('worker {0} not run'.format(worker_id))
    #                 return res.set_end()
    #
    #     worker_id = buject_id
    #     config_list = BubotConfig.get_available_worker()
    #     config = config_list['SimpleWorker']
    #     config['buject'] = {buject_id: {}}
    #     await self.start_worker(worker_id, config)
    #     return res.set_end()
    #
    # async def close_buject(self, buject_id):
    #     await self.send_request('close', receiver=buject_id)
    #
    # async def action_get_active_buject(self):
    #     return await self.redis.hgetall_asdict('buject:param')
    #
    # async def action_get_active_worker(self):
    #     return await self.redis.hgetall_asdict('worker:param')


async def authorize(app, handler):
    async def middleware(request):
        session = await get_session(request)
        if session.get("user"):
            return await handler(request)
        else:
            # auth = 0
            try:
                if issubclass(handler, Ui) and handler.need_auth(request):
                    raise HTTPFound("{0}?redirect={1}".format(app['bubot'].get_param('login_url'), request.path))
                    # auth = request.app['ui'][re.findall('^/ui/(.*)/', request.path)[0]]['param']['auth']
            finally:
                pass
                # if auth:
                # url = request.app.router['login'].url()

        return await handler(request)

    return middleware
