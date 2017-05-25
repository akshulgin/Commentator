# -*- coding: utf-8 -*-

from glob import glob  # функция, которая находит список подходящих файлов, подходящих шаблону
import os
from codecs import open
import re

def clean(text):
    '''Убирает из текста все знаки, приводит к нижнему регистру, возвращает список слов'''
    text = text.replace('.', ' ').strip().lower()
    li = text.split()
    li = [n.strip(',') for n in li]
    return li

def song_link(song_name):
    '''Прокладывает путь к песне'''
    return os.path.join(os.path.dirname(__file__), u'catalog', song_name.lower()+u'.txt')

def get_songs_list():
    links = glob(song_link("*"))
    songs = [os.path.basename(n).split(u".")[0] for n in links]
    return songs

def get_song(song_name):
    with open(song_link(song_name), encoding='utf-8') as f:
        text = f.read()
    return re.sub('[\n]+', '\n', text)
    
def if_contains(li, forli):
    ''' Отвечает на вопрос, содержит ли список li все элементы из forli '''
    for n in forli:
        if not n in li:
            return False
    return True

def get_all_songs():
    dic = {}
    for name in get_songs_list():
        dic[name] = get_song(name)
    return dic

def search_songs(words):
    songs = []  # собираем сюда тексты песен
    for name in get_songs_list():
        song = [clean(get_song(name)), name]
        songs.append(song)
    words = clean(words)
    good = []
    for song in songs:
        if if_contains(song[0], words):
            good.append(song[1])
    return good

def renew_song(song_name, text, delete=False):
    if delete:
        os.remove(song_link(song_name))
    text = re.sub('([\\n]+)', '\\n', text)  # убираем повторяющиеся переносы строки
    with open(song_link(song_name), 'w', encoding='utf-8') as f:
        f.write(text)
    
        



