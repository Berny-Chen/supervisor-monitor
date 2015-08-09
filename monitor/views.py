import os
from .models import *
from .supervisor import *
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone

# Create your views here.


def index(request):
    """
    site entry

    :param request:
    :return:
    """
    if 'ip' in request.GET and 'port' in request.GET:
        # render by specify ip and port
        return index_render(request, request.GET['ip'], request.GET['port'])
    else:
        # try to render the first server in first group
        group = SupervisorServerGroup.objects.first()
        server = SupervisorServer.objects.filter(group=group).first()

        if server:
            context = {
                'ip': server.ip,
                'port': server.port,
                'cur_group': group,
            }
            return index_render(request, server.ip, server.port, context)
        else:
            return render(request, 'monitor/index.html')


def index_render(request, ip, port, context=None):
    """
    index render by specify ip and port

    :param request:
    :param ip:
    :param port:
    :param context:
    :return:
    """
    if context is None:
        context = {}

    server = SupervisorServer.objects.get(ip=ip, port=port)

    supervisor = SupervisorClient(
        server.ip,
        server.port,
        server.username,
        server.password,
    )

    all_process_info = supervisor.call('getAllProcessInfo')
    all_process = {process['group']: [] for process in all_process_info}

    # get warning(not running) process info
    warning_process = []

    for process in all_process_info:
        all_process[process['group']].append(process)

        # as u can see, this is hard code :(
        if process['statename'] != 'RUNNING':
            warning_process.append(process)

    # check not None

    context['all_process'] = all_process
    context['warning_process'] = warning_process

    return render(request, 'monitor/index.html', context)


def xmlrpc(request):
    """
    supervisor xmlrpc

    :param request:
    :return:
    """
    server = SupervisorServer.objects.get(ip=request.GET['ip'])

    supervisor = SupervisorClient(
        server.ip,
        server.port,
        server.username,
        server.password,
    )

    method = request.GET['method']

    if 'params' in request.GET:
        params = request.GET['params'].split(',')
        return HttpResponse(supervisor.call(method, *params))
    else:
        return HttpResponse(supervisor.call(method))


def config(request):
    """
    config file render

    :param request:
    :return:
    """
    ip = request.GET['ip']
    port = request.GET['port']

    # get all config files on servers
    server = SupervisorServer.objects.get(ip=ip, port=port)
    config_files = SupervisorConfigFile.objects.filter(server=server)

    # get current config file
    config_file_id = request.GET.get('config_file_id', 0)

    if config_file_id:
        cur_config_file = SupervisorConfigFile.objects.get(id=config_file_id)
    else:
        cur_config_file = config_files.first()

    # get all config sections in current config file
    config_sections = SupervisorConfigSection.objects.filter(
        file=cur_config_file
    )

    # load the config section values(json format)
    for section in config_sections:
        section.values = json.loads(
            section.values,
            object_pairs_hook=OrderedDict
        ).items()

    # get section values settings
    section_values = SupervisorSectionValue.objects.filter(is_display=True)

    context = {
        'cur_config_file': cur_config_file,
        'config_files': config_files,
        'config_sections': config_sections,
        'section_values': section_values,
    }

    return render(request, 'monitor/config.html', context)


def config_admin(request):
    """
    config section admin

    :param request:
    :return:
    """
    config_file_id = request.GET['config_file_id']
    action = request.GET['action']
    param = json.loads(request.GET['param'])

    # check param
    for key in param:
        if param[key] == '':
            return HttpResponse(key + ': can not be empty')

    # add section
    if action == 'add':
        section = SupervisorConfigSection()
        section.name = param['section_name']
        section.file = SupervisorConfigFile.objects.get(id=config_file_id)
        section.values = param
        section.save()

    # update section
    elif action == 'update':
        section = SupervisorConfigSection.objects.get(id=param['section_id'])
        section.name = param['section_name']
        section.values = param
        section.save()  # auto remove irrelevant key in values when save

    # delete section
    elif action == 'delete':
        section = SupervisorConfigSection.objects.get(id=param['section_id'])
        section.delete()

    # update config file
    config_file = SupervisorConfigFile.objects.get(id=config_file_id)
    config_file.is_modified = True
    config_file.last_modified = timezone.now()
    config_file.save()

    # write config file to local host
    directory = os.path.dirname(config_file.get_local_path())

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(config_file.get_local_path(), 'w') as f:
        f.write(config_file.get_content())

    return HttpResponse('Done: ' + timezone.now().strftime('%H:%M:%S'))


def config_sync(request):
    """
    use 'scp' command to synchronize config file

    :param request:
    :return:
    """
    config_file_id = request.GET['config_file_id']
    config_file = SupervisorConfigFile.objects.get(id=config_file_id)
    success_str = 'Success'

    cmd = 'scp %s %s@%s:%s 2>&1 && echo %s' % (
        config_file.get_local_path(),
        settings.USER,
        config_file.server.ip,
        config_file.path,
        success_str,
    )

    output = os.popen(cmd).read()

    # update config file
    if output.strip() == success_str:
        config_file.is_modified = False
        config_file.sync_time = timezone.now()
        config_file.save()

    return HttpResponse(output.replace('\n', '<br />'))


def config_reload(request):
    """
    use supervisorctl update to reload config

    :param request:
    :return:
    """
    server = SupervisorServer.objects.get(ip=request.GET['ip'])

    cd_cmd = 'cd %s' % settings.FAB_FILE_DIR

    fab_cmd = 'fab user_host:%s,%s reload_config:username=%s,password=%s' % (
        settings.USER,
        server.ip,
        server.username,
        server.password,
    )

    output = os.popen('%s && %s' % (cd_cmd, fab_cmd)).read()

    return HttpResponse(output.replace('\n', '<br />'))
