from tkinter import *
import pokemonapi as pk


def get_pokemon():
    response = requests.get('https://pokeapi.co/api/v2/pokemon-form/151/')
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


print(get_pokemon())
sys.exit(0)

main_window = Tk()

main_window.mainloop()
