#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of movie-down.
# https://github.com/Akhail/movie-down

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2017, Michel Betancourt <MichelBetancourt23@gmail.com>

import os
import sys
import json
import webbrowser
from tebless.widgets import Window, FilterMenu, Label
from movie_down.get_links import get_links

@Window.decorator
def main(window):
    HEIGHT = window.height
    data = {}

    if len(sys.argv) > 1:
        file_url = sys.argv[1]
    else:
        user = os.path.expanduser("~")
        file_url = '.links-movies.json'
        file_url = os.path.join(user, file_url)
    try:
        with open(file_url) as file:
            data = json.load(file)
    except IOError:
        get_links(store=window.store)
        with open(file_url, 'w') as file:
            json.dump(window.store.movies, file, indent=2)
            data = window.store.movies
    inf_label = Label(text='Link', cordy=HEIGHT-2)

    def open_link(name, link):
        inf_label.value = f'Opened {link}'
        webbrowser.open(link + f"#{name}")

    window += FilterMenu({
        'max_len': 20,
        'label': "Pelicula: "
    }, {
        'cordy': 1,
        'limit': HEIGHT-3,
        'items': sorted(data.keys()),
        'on_enter': lambda sender: open_link(sender.value, data[sender.value])
    })

    window += inf_label

if __name__ == '__main__':
    main()
