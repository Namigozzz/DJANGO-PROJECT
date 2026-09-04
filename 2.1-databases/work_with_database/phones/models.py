from django.db import models


class Phone(models.Model):
    # TODO: Добавьте требуемые поля
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    image = models.URLField(max_length=2048)
    release_date = models.DateField()
    lte_exists = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255)
