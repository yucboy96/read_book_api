# Generated by Django 2.1.7 on 2019-04-20 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbTables', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadTracker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('webUrl', models.TextField()),
                ('title', models.CharField(max_length=255)),
                ('sessionId', models.IntegerField()),
                ('readTime', models.IntegerField()),
                ('isSuccess', models.BooleanField()),
                ('modify', models.DateField(auto_now_add=True)),
            ],
        ),
    ]