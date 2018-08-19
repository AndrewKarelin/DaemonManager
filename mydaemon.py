import subprocess
import syslog

daemon = ''


# TODO для систем с высокой нагрузкой можно заменить запуск popen на проверку наличия PID файла
def get_daemon_status():
    status = 'Статус неопределен'
    try:
        prog = subprocess.Popen([daemon, 'status'], stdout=subprocess.PIPE)
        out = str(prog.communicate(timeout=5))
        if 'Active: inactive' in out:
            status = 'Сервис остановлен'
        if 'Active: active' in out:
            status = 'Сервис работает'
    except:
        syslog.syslog('Ошибка при определнии статуса' + daemon + '. Команда status')
    finally:
        return status


def send_command(command):
    try:
        subprocess.Popen([daemon, command])
    except:
        syslog.syslog('Ошибка при управлении ' + daemon + '. Команда ' + command)
