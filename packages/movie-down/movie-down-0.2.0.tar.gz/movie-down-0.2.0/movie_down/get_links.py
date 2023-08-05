# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from queue import Queue
from threading import Thread

from requests import get
from requests.exceptions import BaseHTTPError

from bs4 import BeautifulSoup
from tebless.utils.styles import green, bold
from tebless.widgets import Window, Label

@Window.decorator
def get_links(window):
    tasks = Queue()
    window.store.movies = {}
    [tasks.put(idx) for idx in range(1, 600)]
    def worker(label):
        while not tasks.empty():
            num = tasks.get()
            try:
                web = get(f'http://links.mega-estrenos.com/{num}/')
                bs = BeautifulSoup(web.content, 'html5lib')
                title = bs.h1.contents[0]
                links = bs.find_all('a', {'class':'linkencio'})
                links = [idx.contents[0] for idx in links]
                links = [link for link in links if 'mega.nz' in link]
                if not links:
                    raise AttributeError
                label.value = green("Found: ") + title
                window.store.movies[title] = links[0]
            except (AttributeError, BaseHTTPError, IndexError):
                pass
            finally:
                tasks.task_done()
        tasks.join()
        window.close()
    window += Label(text=bold('Peliculas'), align='center', width=window.width)
    for idx in range(8):
        label = Label(text=f'Worker {idx}', cordy=idx+1)
        thread = Thread(target=worker, args=(label, ))
        thread.start()
        window += label
