#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, session
import pyttsx3
import keyboard
import multiprocessing
import time
from threading import Thread
import threading
import win32com.client as comclt
import pyautogui

app = Flask(__name__)

# engine = pyttsx3.init()

stop_threads = False
all_processes = []
seconds = 0
text = ''
input_text = ''
rate = 0


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/listen', methods=['POST'])
def listen():
    global text
    global input_text
    global seconds
    global rate
    if request.method == 'POST':
        print ('text is' + text)
        print (input_text)
        seconds = time.time()

        # session['seconds'] = seconds

        session['rate'] = 2
        say(text)
        return render_template('result.html')

all_processes = []
text = ''
input_text = ''
rate = 0
seconds = 0


def run():
    while True:
        print ('thread running')
        global stop_threads
        if stop_threads:
            break


def sayFunc(phrase):

        # global rate
        # global seconds

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    voices = engine.getProperty('voices')
    for voice in voices:
        print ('Voice:')
        print (' - ID: %s' % voice.id)
        print (' - Name: %s' % voice.name)
        print (' - Languages: %s' % voice.languages)
        print (' - Gender: %s' % voice.gender)
        print (' - Age: %s' % voice.age)

    en_voice_id="HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hiIN_HemantM"
    print('vid',voices[0].id)
    engine.setProperty('voice', en_voice_id)

    engine.setProperty('rate', 150)
    rate = 2
    engine.say(phrase)
    print ('gs', seconds)
    engine.runAndWait()


def say(phrase):
    if __name__ == '__main__':
        p = multiprocessing.Process(target=sayFunc, args=(phrase, ))

        # p = threading.Thread(target=sayFunc, args=(phrase,))

        p.start()
        all_processes.append(p)
        while p.is_alive():
            if keyboard.is_pressed('q'):
                p.terminate()
            else:
                continue
        p.join()


@app.route('/pause', methods=['POST'])
def pause():
    global text
    global input_text
    global rate
    global seconds
    print ('pp', seconds)
    for process in all_processes:
        process.terminate()

    print ('time', time.time())
    seconds = time.time() - seconds

    # print("sessionss11",session['seconds'])
    # print("sessionss",session.get('seconds'))

    print ('ss', seconds)
    print ('rate', rate)
    session.pop('seconds', None)
    word_count = int(seconds * 2.5)+2
    print ('wc', word_count)
    text = text[word_count:]
    print ('pause ' + text)

    # say(text)

    return render_template('result.html')


@app.route('/stop', methods=['POST'])
def stop():
    global text
    global input_text
    for process in all_processes:
        process.terminate()
    session.pop('seconds', None)
    #print ('fikes', session['file'])
    text = input_text
    return render_template('result.html')


@app.route('/my-link/')
def my_link():
    pyttsx3.engine.Engine.stop(engine)
    pyttsx3.driver.DriverProxy.setBusy(engine, busy=False)


@app.route('/nextpage', methods=['POST'])
def nextpage():
    if request.method == 'POST':
        global text
        global input_text
        #session['file'] = request.form['file']
        print ('fileu', request.files['file'])
        f = request.files['file']

        # f = open(request.form['file'], encoding="utf8")

        text = f.read()
        text = text.decode('utf-8')

        # print("trtrt",text.decode("utf-8") )

        text = text.replace('\n', ' ')
        input_text = text
        return render_template('result.html')

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
