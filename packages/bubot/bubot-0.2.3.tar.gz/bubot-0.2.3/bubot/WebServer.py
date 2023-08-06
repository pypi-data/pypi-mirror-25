import asyncio
import aiohttp_jinja2
import jinja2
import os
from aiohttp.web import json_response, Application, Response, MsgType, WebSocketResponse, View, HTTPFound
from aiohttp_session import get_session, setup, SimpleCookieStorage
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from bubot.Ui import Ui
from bubot import BubotConfig
from bubot.Bubot import Bubot
from bubot.Action import Action
from aiohttp_session import setup, get_session, session_middleware
import re
from aiohttp_session.cookie_storage import EncryptedCookieStorage


async def authorize(app, handler):
    async def middleware(request):
        session = await get_session(request)    
        if session.get("user"):
            return await handler(request)
        else:
            auth = 0
            try:
                auth = request.app['ui'][re.findall('^/ui/(.*)/', request.path)[0]]['param']['auth']
            except:
                pass
            if auth:
                # url = request.app.router['login'].url()
                raise HTTPFound("/ui/login/index.html?redirect={0}".format(request.path))

        return await handler(request)

    return middleware


class BubotWebServer:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.app = Application(loop=self.loop, middlewares=[session_middleware(SimpleCookieStorage()), authorize])
        self.app['sockets'] = []
        self.app['bubot'] = None
        self.server = None
        self.handler = None
        self.ui = {}

    async def init(self, config_path):
        res = Action("WebServer.init")
        # self.app.router.add_route('*', '/', MainHandler)
        # self.app.router.add_static('/{wildcard:/(.*[.](?=ico$|js$|css$).*$)}', os.path.dirname(aiohttp.__file__))
        # self.app.router.add_route('*', '/login', LoginHandler)
        # aiohttp_debugtoolbar.setup(self.app)
        bubot = Bubot(id=config_path)
        print("Read bubot config")
        res.add_stat(await bubot.read_bubot_config(config_path))
        res.add_stat(await bubot.run())
        # print("Check redis")
        # res.add_stat(await bubot.check_redis())
        # await bubot.redis.flushall()
        # print("Check MongoDB")
        # bubot.get_db()
        self.app['bubot'] = bubot
        # print("Read buject")
        # res.add_stat(await bubot.add_all_buject())
        # print("Run worker")
        # res.add_stat(await bubot.start_all_worker())
        self.app['ui'] = res.add_stat(await self.import_ui_handlers())
        self.handler = self.app.make_handler()
        print("Run web server")
        self.server = await self.loop.create_server(self.handler, '127.0.0.1', self.get_param('web_port'))
        return res.set_end()

    async def import_ui_handlers(self):
        res = Action("WebServer.import_ui_handlers")
        try:
            ui = BubotConfig.get_available_ui()
            ui = BubotConfig.config_to_simple_dict(ui)
        except Exception as e:
            print('Error BubotConfig.get_available_ui(): ', str(e))
            return res.set_end(False)
        self.app.router.add_static("/static", "./static")
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

    async def finish(self):
        for ws in self.app['sockets']:
            ws.close()
        self.app['sockets'].clear()
        await asyncio.sleep(0.1)
        self.server.close()
        await self.handler.finish_connections()
        await self.server.wait_closed()

    def start(self, file_name='Bubot'):
        res = self.loop.run_until_complete(self.init(file_name))
        pass
        print(res.stat)
        try:
            if self.app['bubot'].redis:
                print("Server started at http://127.0.0.1:{0}".format(self.get_param('web_port')))
                self.loop.run_until_complete(self.app['bubot'].handle_get_redis_msg())
            else:
                print("Server started at http://127.0.0.1:{0}".format(self.get_param('web_port')))
                self.loop.run_forever()
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.finish())

    def get_param(self, name):
        return self.app['bubot'].config['param'][name]['value']

