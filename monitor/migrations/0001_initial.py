# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SupervisorConfigFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('path', models.CharField(max_length=300)),
                ('is_modified', models.BooleanField(default=False, db_index=True)),
                ('last_modified', models.DateTimeField(null=True, blank=True)),
                ('sync_time', models.DateTimeField(null=True, blank=True)),
                ('index', models.IntegerField(db_index=True)),
            ],
            options={
                'ordering': ['server_id', 'index'],
                'verbose_name': 'Supervisor Config File',
                'verbose_name_plural': 'Supervisor Config Files',
            },
        ),
        migrations.CreateModel(
            name='SupervisorConfigSection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('values', models.TextField()),
                ('file', models.ForeignKey(to='monitor.SupervisorConfigFile')),
            ],
            options={
                'ordering': ['file__server_id', 'file_id'],
                'verbose_name': 'Supervisor Config Section',
                'verbose_name_plural': 'Supervisor Config Sections',
            },
        ),
        migrations.CreateModel(
            name='SupervisorSectionValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=100)),
                ('key_alias', models.CharField(unique=True, max_length=100)),
                ('value', models.CharField(default=b'', max_length=100, blank=True)),
                ('default', models.CharField(default=b'', max_length=100, blank=True)),
                ('is_display', models.BooleanField(default=False)),
                ('index', models.IntegerField(db_index=True)),
            ],
            options={
                'ordering': ['index'],
                'verbose_name': 'Supervisor Section Value',
                'verbose_name_plural': 'Supervisor Section Values',
            },
        ),
        migrations.CreateModel(
            name='SupervisorServer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.GenericIPAddressField()),
                ('port', models.IntegerField()),
                ('username', models.CharField(default=b'', max_length=100, blank=True)),
                ('password', models.CharField(default=b'', max_length=300, blank=True)),
                ('index', models.IntegerField(db_index=True)),
            ],
            options={
                'ordering': ['group_id', 'index'],
                'verbose_name': 'Supervisor Server',
                'verbose_name_plural': 'Supervisor Servers',
            },
        ),
        migrations.CreateModel(
            name='SupervisorServerGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('index', models.IntegerField(db_index=True)),
                ('remark', models.CharField(max_length=500, blank=True)),
            ],
            options={
                'ordering': ['index'],
                'verbose_name': 'Supervisor Server Group',
                'verbose_name_plural': 'Supervisor Server Groups',
            },
        ),
        migrations.AddField(
            model_name='supervisorserver',
            name='group',
            field=models.ForeignKey(to='monitor.SupervisorServerGroup'),
        ),
        migrations.AddField(
            model_name='supervisorconfigfile',
            name='server',
            field=models.ForeignKey(to='monitor.SupervisorServer'),
        ),
        migrations.AlterUniqueTogether(
            name='supervisorserver',
            unique_together=set([('ip', 'port')]),
        ),
    ]
