import random
import re
from pprint import pprint
import requests
from flask import Flask, jsonify, request

app = Flask('app')

database = 'https://store.ncss.cloud/mel-group3-studybot-planner'

def get_data():
  return requests.get(database)

def post_data(data):
  return requests.post(database, json=data)

def reset_data():
  k = input("Are you sure? (y/n) ")
  data = {
  "frank":{"subjects":{"english":4, "physics":7, "maths":10},
           "weekends": False, 
           "study": [900, 1500]
  }
  }
  if k == 'y':
    post_data(data)

reset_data()

#make( me)* a timetable
@app.route('/make', methods=['POST'])
def make():
  storedData = get_data().json()
  data = request.get_json()
  print(data)
  author = data['author'] or 'liam'
  if 'state' not in data:
    storedData[author] = {}
    post_data(storedData)
    phrases = ["Ok human, i hear you\'re looking to make a timetable ey? i\'ve seen many a travellers try, but none return, luckily you have me to help you!", "Goodevening fine human, i have heard over the airways that you are trying to make a timetable! I have taken it upon myself to help you with this.", "Why hello there human, It is my pleasure to make your acquaintance."]
    intro = random.choice(phrases)
    message = {
      'text': f'{intro} Please enter your subjects and how long you want to study them for {author}.',
      'author': 'Timetabler',
      'state': 'subjects'
    }
    return jsonify(message)
  state = data['state']
  if state == 'subjects':
    storedData = get_data().json()
    data = request.get_json()
    subs = re.split(', | and ', data['text'])
    print(subs)
    subjects = {}
    for sub in subs:
      sub = sub.split(' for ')
      subjects[sub[0]] = sub[1].split()[0]
    pprint(subjects)
    print(author, author in storedData, storedData)
    storedData[author]['subjects'] = subjects
    post_data(storedData)
  # pprint(data)
    message = {
      'text': f'Ok, subjects entered {author}.Would you like to study on weekends?',
      'author': 'Timetabler',
      'state': 'weekend'
    }
    return jsonify(message)  
  elif state == 'weekend': #nice
    storedData = get_data().json()
    data = request.get_json()
    author = data['author'] or 'liam'
    if 'will' in data['text'] or 'yes' in data['text'] or 'can ' in data['text'] or 'yeet' in data['text']:
      weekend = True
    else:
      weekend = False
    storedData[author]['weekends'] = weekend
    post_data(storedData)
    message = {
      'text': f'Ok, what times do you want to study?',
      'author': 'Timetabler',
      'state': 'times'
    }
    return jsonify(message)
  elif state == 'times':
    storedData = get_data().json()
    data = request.get_json()
    author = data['author'] or 'liam'
    times = data['text']
    times = times.split()
    if times[0][-2:] == 'am':
      time1 = int(times[0][0:-2])*100
    else:
      time1 = int(times[0][0:-2])*100+1200
    if times[2][-2:] == 'am':
      time2 = int(times[2][0:-2])*100
    else:
      time2 = int(times[2][0:-2])*100+1200
    storedData[author]['time'] = [time1, time2]
    post_data(storedData)
    message = {
      'text': 'Ok, please type print timetable to see your timetable!!',
      'author': 'Timetabler'
    }
    return jsonify(message)

app.run(host='0.0.0.0', port=8080)

























































"""
#I would like to study (?P<subs>.*)$
@app.route('/subjects', methods=['POST'])
def subjects():
  storedData = get_data().json()
  data = request.get_json()
  subs = re.split(', | and ', data['params']['subs'])
  author = data['author']
  if author not in storedData:
    return jsonify({'text': 'please start from the beginning, no jumping the line. (type make a timetable)',
    'author': 'Timetabler'})  
  subjects = {}
  for sub in subs:
    sub = sub.split(' for ')
    subjects[sub[0]] = sub[1].split()[0]
  pprint(subjects)
  storedData[author]['subjects'] = subjects
  post_data(storedData)
 # pprint(data)
  message = {
    'text': f'Ok, subjects entered {author}.Would you like to study on weekends?',
    'author': 'Timetabler'
  }
  return jsonify(message)
#i [^ ]* study on weekends
@app.route('/weekend', methods=['POST'])
def weekend():
  storedData = get_data().json()
  data = request.get_json()
  author = data['author']
  if author not in storedData:
    return jsonify({'text': 'please start from the beginning, no jumping the line.'})
  if 'will' in data['text']:
    weekend = True
  else:
    weekend = False
  storedData[author]['weekends'] = weekend
  post_data(storedData)
  message = {
    'text': f'Ok, what times do you want to study?',
    'author': 'Timetabler'
  }
  return jsonify(message)
"""