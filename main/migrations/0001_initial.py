# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import re
import django.utils.timezone
import djbase.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('email', models.EmailField(unique=True, max_length=75, verbose_name='Email')),
                ('username', models.CharField(unique=True, max_length=32, verbose_name='Username', validators=[django.core.validators.RegexValidator(regex=re.compile('^[a-z0-9_.-]+$', 2)), django.core.validators.MinLengthValidator(5)])),
                ('first_name', models.CharField(max_length=50, verbose_name='First name')),
                ('middle_name', models.CharField(default='', max_length=50, blank=True)),
                ('last_name', models.CharField(default='', max_length=50, blank=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
                ('gender', models.CharField(default='', max_length=1, blank=True, choices=[('m', 'Male'), ('f', 'Female')])),
                ('birthday', models.DateField(null=True, verbose_name='Date of birth', blank=True)),
                ('description', models.CharField(default='', max_length=512, verbose_name='About', blank=True)),
                ('timezone', models.SmallIntegerField(default=32000)),
                ('verification_code', models.CharField(default=b'e6f2fcb1a430cb601b1727', unique=True, max_length=100)),
                ('is_staff', models.BooleanField(default=False)),
                ('avatar', models.URLField(default='https://thesocietypages.org/socimages/files/2009/05/vimeo.jpg')),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_disabled', models.BooleanField(default=False, verbose_name='Is deactivated')),
            ],
            options={
                'db_table': 'account',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ActionRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Activate email'), (2, 'Password reset')])),
                ('hashed', djbase.models.FixedCharField(max_length=40)),
                ('expiry', models.DateTimeField()),
                ('account', models.ForeignKey(related_name='+', to='main.Account', db_index=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField(max_length=2000)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('district_name', models.CharField(max_length=50, blank=True)),
                ('city_id', models.ForeignKey(to='main.City', on_delete=django.db.models.deletion.PROTECT, db_index=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, blank=True)),
                ('address', models.CharField(max_length=100)),
                ('price_morning', models.FloatField()),
                ('price_afternoon', models.FloatField()),
                ('price_evening', models.FloatField()),
                ('phone_number', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
                ('rating', models.FloatField()),
                ('lat', models.DecimalField(max_digits=9, decimal_places=6)),
                ('lng', models.DecimalField(max_digits=9, decimal_places=6)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('deleted', models.DateTimeField(auto_now_add=True)),
                ('size', models.CharField(blank=True, max_length=1, choices=[('5', '5'), ('7', '7')])),
                ('district_id', models.ForeignKey(to='main.District', on_delete=django.db.models.deletion.PROTECT, db_index=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('maximum_players', models.SmallIntegerField(default=12)),
                ('price', models.FloatField()),
                ('sub_match', models.SmallIntegerField(default=1)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('slots', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('is_verified', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('deleted', models.DateTimeField(auto_now_add=True)),
                ('field_id', models.ForeignKey(to='main.Field', on_delete=django.db.models.deletion.PROTECT, db_index=False)),
                ('host_id', models.ForeignKey(to='main.Account')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source_size_og', models.URLField(blank=True)),
                ('source_size_lg', models.URLField(blank=True)),
                ('source_size_md', models.URLField(blank=True)),
                ('source_size_sm', models.URLField(blank=True)),
                ('source_size_xs', models.URLField(blank=True)),
                ('source_size_ss', models.URLField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('verification_code', models.CharField(default=b'77cec3655cda5c3ba06f55', unique=True, max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('deleted', models.DateTimeField(auto_now_add=True)),
                ('match_id', models.ForeignKey(to='main.Match')),
                ('user_id', models.ForeignKey(to='main.Account')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='field',
            name='photo',
            field=models.ForeignKey(related_name='photos', default=1, to='main.Photo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='match_object',
            field=models.ForeignKey(to='main.Match', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(editable=False, to='main.Account', on_delete=django.db.models.deletion.PROTECT, db_index=False),
            preserve_default=True,
        ),
        migrations.AlterIndexTogether(
            name='comment',
            index_together=set([('user', 'date_created')]),
        ),
        migrations.AlterUniqueTogether(
            name='actionrequest',
            unique_together=set([('account', 'type')]),
        ),
        migrations.AddField(
            model_name='account',
            name='district_id',
            field=models.ForeignKey(to='main.District', on_delete=django.db.models.deletion.PROTECT, db_index=False),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='ActivateEmailRequest',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('main.actionrequest',),
        ),
    ]
