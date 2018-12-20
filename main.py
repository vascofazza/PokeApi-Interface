import io
from io import StringIO
from tkinter import *

import PIL
from PIL import ImageTk

import pokemonapi as pk

api = pk.PokemonApi()

window = Tk()

window.title("PokeApi Interface")

txt = Entry(window, width=10)

txt.grid(column=0, row=0)

name_label = Label(window, text="Nome: ")

name_label.grid(column=0, row=1)

tipo_label = Label(window, text="Tipo: ")

tipo_label.grid(column=0, row=2)

front_sprite_label = Label(window)

front_sprite_label.grid(column=1, row=1)

back_sprite_label = Label(window)

back_sprite_label.grid(column=1, row=2)

front_sprite_s_label = Label(window)

front_sprite_s_label.grid(column=2, row=1)

back_sprite_s_label = Label(window)

back_sprite_s_label.grid(column=2, row=2)

def load_sprite(name, sprite):
    label = None
    if 'front' in name:
        if 'shiny' in name:
            label = front_sprite_s_label
        else:
            label = front_sprite_label
    elif 'back' in name:
        if 'shiny' in name:
            label = back_sprite_s_label
        else:
            label = back_sprite_label
    bytes = io.BytesIO(sprite)
    image = PIL.ImageTk.Image.open(bytes)
    img = PIL.ImageTk.PhotoImage(image)
    label.configure(image=img)
    label.image = img

def clicked():
    pokemon = api.get_pokemon(poke_name=txt.get())
    name_label.configure(text='Nome: ' + pokemon.name)
    tipo_label.configure(text='Tipo: ' + pokemon.get_tipo())
    for name, sprite in pokemon.get_sprites().items():
        load_sprite(name, sprite)

btn = Button(window, text="Ottieni", command=clicked)

btn.grid(column=1, row=0)

window.mainloop()
