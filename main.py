import random
import re
from pprint import pprint
import requests
from flask import Flask, jsonify, request
app = Flask('app')

@app.route('/make', methods=['POST'])
def make():
  data = request.get_json()
  author = data['author']
  phrases = ["Ok human, i hear you\'re looking to make a timetable ey? i\'ve seen many a travellers try, but none return, luckily you have me to help you!", "Goodevening fine human, i have heard over the airways that you are trying to make a timetable! I have taken it upon myself to help you with this.", "Why hello there human, It is my pleasure to make your acquaintance."]
  intro = random.choice(phrases)
  message = {
    'text': f'{intro} Please enter your subjects and how long you want to study them for {author}.',
    'author': 'timetabler'
  }
  return jsonify(message)


@app.route('/subjects', methods=['POST'])
def subjects():
  data = request.get_json()
  subs = re.split(', | and ', data['params']['subs'])
  author = data['author']
  subjects = {}
  for sub in subs:
    sub = sub.split(' for ')
    subjects[sub[0]] = sub[1].split()[0]
  
  pprint(subjects)
 # pprint(data)
  message = {
    'text': f'Ok, subjects entered {author}.Would you like to study on weekends?'
  }
  return jsonify(message)

@app.route('/weekend', methods=['POST'])
def weekend():
  data = request.get_json()
  author = data['author']
  if 'will' in data['text']:
    weekend = True
  else:
    weekend = False
  message = {
    'text': f'Ok that\'s all i\'ve done',
    'author': 'timetabler'
  }
  
  return jsonify(message)

app.run(host='0.0.0.0', port=8080)