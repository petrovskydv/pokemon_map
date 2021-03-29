from django.db import models


class Pokemon(models.Model):
    title = models.CharField('Название', max_length=200)
    title_en = models.CharField('Название англ.', max_length=200, blank=True)
    title_jp = models.CharField('Название яп.', max_length=200, blank=True)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Изображение', null=True, blank=True)
    previous_evolution = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                           verbose_name='Из кого эволюционирует')

    def __str__(self):
        return self.title

    def get_image_url(self):
        return self.image.url if self.image else None


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Покемон')
    lat = models.FloatField('Широта')
    lon = models.FloatField('Долгота')
    appeared_at = models.DateTimeField('Время появления', null=True, blank=True)
    disappeared_at = models.DateTimeField('Время исчезновения', null=True, blank=True)
    level = models.IntegerField('Уровень', default=0, blank=True)
    health = models.IntegerField('Здоровье', default=0, blank=True)
    strength = models.IntegerField('Атака', default=0, blank=True)
    defence = models.IntegerField('Защита', default=0, blank=True)
    stamina = models.IntegerField('Выносливость', default=0, blank=True)

    def __str__(self):
        return f'{self.pokemon.title} level:{self.level} lat:{self.lat} lon:{self.lon}'
