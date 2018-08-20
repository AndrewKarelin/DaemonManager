import json
import os.path
import syslog


def load_config():
    def_config = {'flag_state': 'checked', 'host_name': 'localhost', 'port': 8080,
                  'daemon_name': r'/etc/init.d/cups', 'poll_interval': 5}

    config_file_name = os.getcwd() + '/config.json'
    try:
        with open(config_file_name, 'r') as f:
            config = json.load(f)
        syslog.syslog('Конфигурация загружена ' + config_file_name + '  ' + str(config))
    except:
        config = def_config
        syslog.syslog('Конфигурация по умолчанию ' + str(config))
    return config


def save_config(config):
    config_file_name = os.getcwd() + '/config.json'
    try:
        with open(config_file_name, 'w') as f:
            json.dump(config, f)
        syslog.syslog('Конфигурация сохранена ' + config_file_name + '  ' + str(config))
    except:
        syslog.syslog('Ошибка сохранения конфигурации  ' + config_file_name + '  ' + str(config))
