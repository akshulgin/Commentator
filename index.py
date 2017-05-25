# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, session
from songs import get_songs_list, get_song, get_all_songs, renew_song, search_songs
import vk_api

app = Flask(__name__)
app.debug = True  # 
app.secret_key = "hbfashubudshvbhsduvubsvbывusubv"

@app.route("/")
def index():
    return render_template("index.html", songs=get_songs_list())

@app.route("/song/<name>")
def song(name):
    return render_template("song.html", song=get_song(name), name=name.capitalize())

@app.route("/search")
def search():
    return render_template("search.html", songs=search_songs(request.args['key']))

@app.route("/a")
def a():
    return render_template("admin.html", songs=get_all_songs())

@app.route("/change_song/<name>")
def change_song(name):
    renew_song(name, request.args['text'])
    return redirect('/a')

@app.route("/add_song")
def add_song():
    renew_song(request.args['name'], request.args['text'])
    return redirect('/a')

@app.route("/login")
def login():
    return render_template("login.html", alert=request.args.get('alert', ""))

@app.route("/log")
def log():
    vk = vk_api.VkApi(request.args['login'], request.args['password'])
    try:
        vk.auth()
    except vk_api.ApiError:
        return redirect('/login?alert=Wrong+data')
    session['token'] = vk.token['access_token']
    return redirect('/choice?name='+session['song'])

@app.route("/choice")
def choice():
    session['song'] = request.args['name']
    if 'token' in session:
        vk = vk_api.VkApi(token=session['token'])
        friends = vk.method('friends.get', {'order': 'hints', 'fields': 'can_post'})['items']
        return render_template('choice.html', friends=[n for n in friends if n['can_post'] == 1])
    else:
        return redirect('/login')

@app.route("/send")
def send():
    if 'token' in session:
        vk = vk_api.VkApi(token=session['token'])
        try:
            resp = vk.method('wall.post', {'owner_id': request.args['ui'],
                                           'message': get_song(session['song'])})
            return render_template("success.html", link=request.args['ui']+'_'+str(resp['post_id']),
                                   name=session['song'])
        except vk_api.ApiError:
            return "Ooops, error. Probably the wall is private. <a href='/choice'>Back</a>"
    else:
        return redirect('/login')    

if __name__=="__main__":
    app.run('127.0.0.1', 80)
