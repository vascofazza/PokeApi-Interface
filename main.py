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

peso_label = Label(window, text="Peso: ")

peso_label.grid(column=0, row=3)

altezza_label = Label(window, text="Altezza: ")

altezza_label.grid(column=0, row=4)

front_sprite_label = Label(window)

front_sprite_label.grid(column=1, row=1)

back_sprite_label = Label(window)

back_sprite_label.grid(column=1, row=2)

front_sprite_s_label = Label(window)

front_sprite_s_label.grid(column=2, row=1)

back_sprite_s_label = Label(window)

back_sprite_s_label.grid(column=2, row=2)

mosse_box = Listbox(window, height=10)

mosse_box.grid(column=0, row=5)

stat_box = Listbox(window, height=10)

stat_box.grid(column=1, row=5)

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
    altezza_label.configure(text='Altezza: '+str(pokemon.height))
    peso_label.configure(text='Peso: ' + str(pokemon.weight))
    for idx, mossa in enumerate(pokemon.get_mosse()):
        mosse_box.insert(idx, mossa)
    for idx, spec in enumerate([name+" - " + str(spec) for name, spec in pokemon.get_stats().items()]):
        stat_box.insert(idx, spec)
    #mosse_box.configure(listvariable=pokemon.get_mosse())
    #stat_box.configure(listvariable=[name+" - " + str(spec) for name, spec in pokemon.get_stats().items()])
    for name, sprite in pokemon.get_sprites().items():
        load_sprite(name, sprite)

btn = Button(window, text="Ottieni", command=clicked)

btn.grid(column=1, row=0)

window.mainloop()
