from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stopwatch', '0046_auto_20240612_1805'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailHeartbeat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'get_latest_by': 'sent_at',
            },
        ),
    ]
