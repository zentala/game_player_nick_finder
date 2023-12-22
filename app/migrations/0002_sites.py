from django.db import migrations
from django.conf import settings

def create_or_update_site(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    site_id = settings.SITE_ID

    # Tworzy nowy obiekt Site lub aktualizuje istniejący
    site, created = Site.objects.update_or_create(id=site_id, defaults={
        'domain': 'gpnf.zentala.io',
        'name': 'Game Player Nick Finder'
    })

class Migration(migrations.Migration):

    dependencies = [
        # Zależności; upewnij się, że wskazujesz na poprzednią migrację w Twojej aplikacji
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_or_update_site),
    ]
