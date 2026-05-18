from django.db import migrations


GENRES = [
    ("blues", "Blues"),
    ("classical", "Classical"),
    ("country", "Country"),
    ("disco", "Disco"),
    ("hiphop", "Hip-hop"),
    ("jazz", "Jazz"),
    ("metal", "Metal"),
    ("pop", "Pop"),
    ("reggae", "Reggae"),
    ("rock", "Rock"),
]


def seed(apps, schema_editor):
    Genre = apps.get_model("classification", "Genre")
    for slug, name in GENRES:
        Genre.objects.get_or_create(slug=slug, defaults={"name": name, "description": ""})


def unseed(apps, schema_editor):
    Genre = apps.get_model("classification", "Genre")
    Genre.objects.filter(slug__in=[s for s, _ in GENRES]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("classification", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
