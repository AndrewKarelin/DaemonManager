import asyncio
import syslog

import aiohttp_jinja2
import jinja2
from aiohttp import web

import mydaemon

button_state = {'checked': '', '': 'disabled'}
flag_state = {'disable': '', 'enable': 'checked'}


async def handle_status(request):
    status = mydaemon.get_daemon_status()

    while request.app['status'] == status:
        await asyncio.sleep(request.app['poll_interval'])
        status = mydaemon.get_daemon_status()

    request.app['status'] = status
    return web.Response(text=status)


async def render_page(request):
    context = {'disabled': button_state[request.app['checked']],
               'checked': request.app['checked']}
    return aiohttp_jinja2.render_template('index.html', request, context)


async def handle_command(request):
    command = request.match_info['command']
    syslog.syslog('Have command ' + command)
    request.app['status'] = 'Определяю статус'
    if command in ['disable', 'enable']:
        request.app['checked'] = flag_state[command]
    elif command in ['start', 'restart', 'stop']:
        mydaemon.send_command(command)
    raise web.HTTPFound('/')


def init_web(config):
    app = web.Application()

    app['status'] = 'Определяю статус'
    app['checked'] = config['flag_state']
    app['poll_interval'] = config['poll_interval']

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

    app.add_routes([web.get('/', render_page),
                    web.get('/status', handle_status),
                    web.get('/{command}', handle_command)
                    ])
    return app
