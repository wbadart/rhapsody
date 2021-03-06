# Generated by Django 2.0.3 on 2018-03-27 22:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('album_type', models.CharField(choices=[('A', 'album'), ('S', 'single'), ('C', 'compilation')], default='A', max_length=1)),
                ('spotify_id', models.CharField(max_length=22, primary_key=True, serialize=False)),
                ('label', models.CharField(default='', max_length=30)),
                ('name', models.CharField(default='', max_length=30)),
                ('release_date', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('spotify_id', models.CharField(max_length=22, primary_key=True, serialize=False)),
                ('popularity', models.IntegerField(null=True)),
                ('name', models.CharField(default='', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Concert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('artists', models.ManyToManyField(to='rhapsody_web.Artist')),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('spotify_id', models.CharField(max_length=22, primary_key=True, serialize=False)),
                ('collaborative', models.BooleanField(default=False)),
                ('description', models.CharField(default='', max_length=5000)),
                ('name', models.CharField(default='', max_length=30)),
                ('public', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='RadioStation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('spotify_id', models.CharField(max_length=22, primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=30)),
                ('album', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rhapsody_web.Album')),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rhapsody_web.Artist')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=30, unique=True)),
                ('spotify_id', models.CharField(max_length=22, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='rhapsody_web.User')),
            ],
            bases=('rhapsody_web.user',),
        ),
        migrations.CreateModel(
            name='Regular',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='rhapsody_web.User')),
            ],
            bases=('rhapsody_web.user',),
        ),
        migrations.AddField(
            model_name='user',
            name='album',
            field=models.ManyToManyField(to='rhapsody_web.Album'),
        ),
        migrations.AddField(
            model_name='user',
            name='artist',
            field=models.ManyToManyField(to='rhapsody_web.Artist'),
        ),
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rhapsody_web.User'),
        ),
        migrations.AddField(
            model_name='user',
            name='genre',
            field=models.ManyToManyField(to='rhapsody_web.Genre'),
        ),
        migrations.AddField(
            model_name='user',
            name='playlist_followed',
            field=models.ManyToManyField(to='rhapsody_web.Playlist'),
        ),
        migrations.AddField(
            model_name='user',
            name='radio_station',
            field=models.ManyToManyField(to='rhapsody_web.RadioStation'),
        ),
        migrations.AddField(
            model_name='user',
            name='song',
            field=models.ManyToManyField(to='rhapsody_web.Song'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rhapsody_web.User'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='songs',
            field=models.ManyToManyField(to='rhapsody_web.Song'),
        ),
        migrations.AddField(
            model_name='album',
            name='artists',
            field=models.ManyToManyField(to='rhapsody_web.Artist'),
        ),
        migrations.AddField(
            model_name='album',
            name='genres',
            field=models.ManyToManyField(to='rhapsody_web.Genre'),
        ),
    ]
