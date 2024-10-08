# Generated by Django 4.1 on 2023-11-10 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_prompt_original_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='OutputImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('output_image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('prompt', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='app.prompt')),
            ],
        ),
    ]
