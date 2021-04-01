import folium
from django.http import HttpResponseNotFound
from django.shortcuts import render

from pokemon_entities.models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]


def add_pokemon(folium_map, lat, lon, image_url):
    if image_url:
        icon = folium.features.CustomIcon(
            image_url,
            icon_size=(50, 50),
        )
    else:
        icon = folium.Icon(color="green")

    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons_entity = PokemonEntity.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons_entity:
        img_url = None
        if pokemon_entity.pokemon.image:
            img_url = request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            img_url
        )

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.get_image_url(),
            'title_ru': pokemon.title,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    pokemon_description = {
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'img_url': pokemon.get_image_url(),
    }
    if pokemon.previous_evolution:
        pokemon_description['previous_evolution'] = get_evolution_pokemon(pokemon.previous_evolution)

    next_evolution_pokemon = pokemon.next_evolution.first()
    if next_evolution_pokemon:
        pokemon_description['next_evolution'] = get_evolution_pokemon(next_evolution_pokemon)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = pokemon.entities.all()
    for pokemon_entity in pokemon_entities:
        img_url = None
        if pokemon_entity.pokemon.image:
            img_url = request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            img_url
        )

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon_description})


def get_evolution_pokemon(pokemon):
    return {
        'title_ru': pokemon.title,
        'pokemon_id': pokemon.id,
        'img_url': pokemon.get_image_url()
    }
