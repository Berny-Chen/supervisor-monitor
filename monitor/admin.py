from django.contrib import admin
from .models import *

# Register your models here.


class SupervisorConfigFileInline(admin.TabularInline):
    model = SupervisorConfigFile
    fields = ('path', 'name', 'index', 'modified')
    extra = 1


class SupervisorServerAdmin(admin.ModelAdmin):
    list_display = ('ip', 'port', 'group', 'username', 'password', 'index')
    fields = ('group', 'ip', 'port', 'username', 'password', 'index')
    inlines = [SupervisorConfigFileInline]


class SupervisorServerInline(admin.TabularInline):
    model = SupervisorServer
    extra = 1


class SupervisorServerGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'index', 'remark')
    inlines = [SupervisorServerInline]


class SupervisorConfigSectionInline(admin.TabularInline):
    model = SupervisorConfigSection
    fields = ('name', 'values')
    extra = 1


class SupervisorConfigFileAdmin(admin.ModelAdmin):
    list_display = (
        'path', 'server', 'name', 'last_modified',
        'sync_time', 'modified', 'index'
    )

    fields = ('path', 'server', 'name', 'index', 'modified')
    inlines = [SupervisorConfigSectionInline]


class SupervisorConfigSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'file')


class SupervisorSectionValueAdmin(admin.ModelAdmin):
    list_display = (
        'key', 'key_alias', 'value', 'default', 'index', 'display',
    )

    fields = ('key', 'key_alias', 'value', 'default', 'index', 'display',)


admin.site.register(SupervisorServer, SupervisorServerAdmin)
admin.site.register(SupervisorServerGroup, SupervisorServerGroupAdmin)
admin.site.register(SupervisorConfigFile, SupervisorConfigFileAdmin)
admin.site.register(SupervisorConfigSection, SupervisorConfigSectionAdmin)
admin.site.register(SupervisorSectionValue, SupervisorSectionValueAdmin)
