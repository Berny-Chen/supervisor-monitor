from django import template
from monitor.models import SupervisorSectionValue

register = template.Library()


@register.filter(name='get_label_type')
def get_label_type(value):
    label_type = {
        'EXITED': 'label-default',
        'RUNNING': 'label-success',
        'STARTING': 'label-warning',
        'STOPPED': 'label-danger',
    }

    return label_type[value] if value in label_type else 'label-default'


@register.filter(name='get_key_alias')
def get_key_alias(value):
    alias = {
        i.key: i.key_alias for i in SupervisorSectionValue.objects.all()
        }

    return alias[value]
