from fabric.api import env
from fabric.api import run


def user_host(user, host):
    """
    set user and hosts env

    :param user:
    :param host:
    :return:
    """
    env.user = user
    env.hosts = [host]


def reload_config(username=None, password=None):
    """
    reload config by supervisorctl update command

    :param username:
    :param password:
    :return:
    """
    if username and password:
        run('supervisorctl -u %s -p %s update' % (username, password))
    else:
        run('supervisorctl update')
