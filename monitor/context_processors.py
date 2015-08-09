from .models import SupervisorServer
from .models import SupervisorServerGroup


def default(request):
    """
    default context

    :param request:
    :return:
    """
    context = {}

    # ger current group
    if 'ip' in request.GET and 'port' in request.GET:
        context['ip'] = request.GET['ip']
        context['port'] = request.GET['port']

        server = SupervisorServer.objects.get(
            ip=context['ip'],
            port=context['port']
        )

        context['cur_group'] = server.group

    # for nav bar
    groups = SupervisorServerGroup.objects.all()

    for group in groups:
        setattr(group, 'servers', SupervisorServer.objects.filter(group=group))

    context['groups'] = groups

    return context
