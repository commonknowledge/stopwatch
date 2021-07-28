# Generated by Django 3.2.5 on 2021-07-27 13:09

from django.conf import settings
from django.db import migrations, models
import wagtail.core.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):
    dependencies = [
        ('home', '0005_auto_20210728_0856'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ListPage',
            new_name='LandingPage',
        ),
        migrations.CreateModel(
            name='ListPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=models.deletion.CASCADE,
                 parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
