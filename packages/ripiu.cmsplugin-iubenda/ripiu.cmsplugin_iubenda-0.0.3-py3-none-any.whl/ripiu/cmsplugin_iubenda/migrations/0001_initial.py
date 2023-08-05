# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='IubendaStandardPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(primary_key=True, serialize=False, auto_created=True, related_name='cmsplugin_iubenda_iubendastandardpluginmodel', parent_link=True, to='cms.CMSPlugin')),
                ('user_id', models.CharField(verbose_name='user id', max_length=400, default='', help_text='Your user ID on Iubenda')),
            ],
            options={
                'verbose_name': 'Iubenda button (standard)',
                'verbose_name_plural': 'Iubenda buttons (standard)',
            },
            bases=('cms.cmsplugin',),
        ),
    ]
