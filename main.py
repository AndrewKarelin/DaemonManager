import syslog

from aiohttp import web

import myconfig
import mydaemon
import myweb


def main():
    syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_DAEMON)
    syslog.syslog('Web server managing daemon starting.')

    app_config = myconfig.load_config()
    mydaemon.daemon = app_config['daemon_name']

    app = myweb.init_web(app_config)

    web.run_app(app, host=app_config['host_name'], port=app_config['port'])

    syslog.syslog('Web server managing ' + app_config['daemon_name'] + ' exiting.')

    app_config['flag_state'] = app['checked']
    myconfig.save_config(app_config)


main()
#
# if __name__ == '__main__':
#     if os.geteuid() == 0:
#         main()
#     else:
#         current_script = os.path.realpath(__file__)
#         subprocess.call(['sudo','-S', 'python3', current_script])
#
