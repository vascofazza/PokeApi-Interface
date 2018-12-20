import requests
import json


class PokemonApi:
    api_url_base = 'https://pokeapi.co/api/v2/'

    def get_pokemon_form(self, pokemon):
        api_pkmn_form = 'pokemon-form/'
        forme = pokemon.data['forms']
        if len(forme) > 0:
            return self._request(api_pkmn_form, url=forme[0]['url'])
        else:
            raise ValueError('Nessun valore specificato')

    def get_pokemon(self, poke_num=0, poke_name=None):
        api_pkmn = 'pokemon'
        if not poke_name:
            poke_name = str(poke_num)
        return Pokemon(self._request(api_pkmn, poke_name))

    def get_pokemon_sprites(self, pokemon):
        pokeform = self.get_pokemon_form(pokemon)
        sprites = pokeform['sprites']
        return {key: self.raw_requests(values) for key, values in sprites.items()}

    def get_evolutions(self, pokemon):
        api_evls = 'evolution-chain'
        result = self._request(api_evls, value=pokemon.id)
        if len(result['chain']['evolves_to']) > 0:
            evolution = result['chain']['evolves_to'][0]['species']['name']
            return self.get_pokemon(poke_name=evolution)
        return None

    def raw_requests(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            raise ConnectionError('Errore durante l\'accesso alle API')

    def _request(self, enty_point, value=None, url=None):
        if url:
            response = requests.get(url)
        elif value:
            if type(value) == int:
                value = str(value)
            response = requests.get(PokemonApi().api_url_base + '/'.join([enty_point, value + '/']))
        else:
            raise ValueError('Nessun valore specificato')
        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            raise ConnectionError('Errore durante l\'accesso alle API')


class Pokemon:
    api = PokemonApi()

    def __init__(self, data):
        self.data = data
        self.name = data['name']
        self.height = data['height']
        self.weight = data['weight']
        self.id = int(data['id'])
        self.order = int(data['order'])

    def get_sprites(self):
        sprites = Pokemon.api.get_pokemon_sprites(self)
        return sprites

    def get_evoluzione(self):
        evoluzione = Pokemon.api.get_evolutions(self)
        return evoluzione

    def get_mosse(self):
        mosse = self.data['moves']
        return [mossa['move']['name'] for mossa in mosse]

    def get_stats(self):
        stats = self.data['stats']
        return {stat['stat']['name']:stat['base_stat'] for stat in stats}

    def get_tipo(self):
        types = self.data['types']
        return '-'.join([type['type']['name'] for type in types])

    def __str__(self):
        return 'Nome: %s\nTipo: %s\nOrdine: %d\nPeso: %s\nAltezza: %s' % (
        self.name, self.get_tipo(), self.order, self.weight, self.height)


if __name__ == '__main__':
    api = PokemonApi()
    for x in range(1, 21):
        pokemon = api.get_pokemon(poke_num=x)
        print(pokemon)
        print(pokemon.get_mosse())
        print(pokemon.get_sprites())
        print(pokemon.get_evoluzione())
        print(pokemon.get_stats())
