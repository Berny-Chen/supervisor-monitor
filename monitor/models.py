import json
from collections import OrderedDict
from django.db import models
from django.conf import settings

# Create your models here.


class SupervisorServerGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)
    index = models.IntegerField(db_index=True)
    remark = models.CharField(max_length=500, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Supervisor Server Group'
        verbose_name_plural = 'Supervisor Server Groups'
        ordering = ['index']


class SupervisorServer(models.Model):
    ip = models.GenericIPAddressField()
    port = models.IntegerField()
    username = models.CharField(max_length=100, default='', blank=True)
    password = models.CharField(max_length=300, default='', blank=True)
    group = models.ForeignKey(SupervisorServerGroup, db_index=True)
    index = models.IntegerField(db_index=True)

    def __str__(self):
        return self.ip

    class Meta:
        unique_together = ('ip', 'port')
        verbose_name = 'Supervisor Server'
        verbose_name_plural = 'Supervisor Servers'
        ordering = ['group_id', 'index']


class SupervisorConfigFile(models.Model):
    server = models.ForeignKey(SupervisorServer)
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=300)
    modified = models.BooleanField(default=False, db_index=True)
    last_modified = models.DateTimeField(blank=True, null=True)
    sync_time = models.DateTimeField(blank=True, null=True)
    index = models.IntegerField(db_index=True)

    def get_content(self):
        """
        get config file content

        :return:
        """
        sections = SupervisorConfigSection.objects.filter(file=self)
        str_list = [section.to_str() for section in sections]
        return '\n\n'.join(str_list)

    def get_local_path(self):
        """
        get the local config file path

        :return:
        """
        return settings.CONFIG_FILE_DIR + '/' + self.server.ip + self.path

    def __str__(self):
        # distinguish same path in different server
        return self.server.ip + ': ' + self.path

    class Meta:
        verbose_name = 'Supervisor Config File'
        verbose_name_plural = 'Supervisor Config Files'
        ordering = ['server_id', 'index']


class SupervisorConfigSection(models.Model):
    file = models.ForeignKey(SupervisorConfigFile)
    name = models.CharField(max_length=100)
    values = models.TextField()

    def save(self, *args, **kwargs):
        """
        remove irrelevant and default value keys

        :param args:
        :param kwargs:
        :return:
        """

        # for admin
        if isinstance(self.values, basestring):
            self.values = json.loads(self.values)

        self.values = json.dumps(self.values_filter(self.values))

        super(SupervisorConfigSection, self).save(*args, **kwargs)

    def to_str(self):
        """
        change section object to config string

        :return:
        """
        rows = ['[program:' + self.name + ']']

        mapping = json.loads(self.values)

        for key in mapping:
            rows.append(key + '=' + mapping[key])

        return '\n'.join(rows)

    @staticmethod
    def values_filter(values):
        """
        remove irrelevant and default value keys

        :param values:
        :return:
        """
        default_values = OrderedDict(
            (i.key, i.default) for i in SupervisorSectionValue.objects.all()
        )

        result = OrderedDict()

        for key, val in default_values.items():
            if key in values and values[key] != val:
                result[key] = values[key]

        return result

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Supervisor Config Section'
        verbose_name_plural = 'Supervisor Config Sections'
        ordering = ['file__server_id', 'file_id']


class SupervisorSectionValue(models.Model):
    key = models.CharField(max_length=100, unique=True)
    key_alias = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=100, blank=True, default='')
    default = models.CharField(max_length=100, blank=True, default='')
    display = models.BooleanField(default=False)
    index = models.IntegerField(db_index=True)

    def __unicode__(self):
        return self.key

    class Meta:
        verbose_name = 'Supervisor Section Value'
        verbose_name_plural = 'Supervisor Section Values'
        ordering = ['-display', 'index']
