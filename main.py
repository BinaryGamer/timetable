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
           "study": [1000, 1500]
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
  if 'state' not in data:   
    author = data['author']
    storedData[author] = {}
    post_data(storedData)
    phrases = ["Ok human, i hear you\'re looking to make a timetable ey? i\'ve seen many a travellers try, but none return, luckily you have me to help you!", "Goodevening fine human, i have heard over the airways that you are trying to make a timetable! I have taken it upon myself to help you with this.", "Why hello there human, It is my pleasure to make your acquaintance."]
    intro = random.choice(phrases)
    message = {
      'text': f'{intro} Please enter your subjects and how long you want to study them for {author}. (subject for x hours, subject2 for x hours and subject3 for x hours).',
      'author': 'Timetabler',
      'state': {'progress': 'subjects', 'author': author}
    }
    return jsonify(message)
  state = data['state']
  if state['progress'] == 'subjects':
    author = state['author']
    storedData = get_data().json()
    data = request.get_json()
    subs = re.split(', | and ', data['text'])
    print(subs)
    subjects = {}
    for sub in subs:
      sub = sub.split(' for ')
      subjects[sub[0]] = int(sub[1].split()[0])
    pprint(subjects)
    print(author, author in storedData, storedData)
    storedData[author]['subjects'] = subjects
    post_data(storedData)
  # pprint(data)
    message = {
      'text': f'Ok, subjects entered {author}.Would you like to study on weekends?',
      'author': 'Timetabler',
      'state': {'progress': 'weekend', 'author': author}
    }
    return jsonify(message)  
  elif state['progress'] == 'weekend': #nice
    author = state['author']
    storedData = get_data().json()
    data = request.get_json()
    text = data['text']
    if 'will' in text or 'yes' in text or 'can ' in text or 'yeet' in text or 'affirm' in text or 'sure' in text or 'sounds good' in text or 'sounds like a plan' in text or 'fine' in text:
      weekend = True
      phraseyboi = 'will'
    else:
      weekend = False
      phraseyboi = 'won\'t'
    storedData[author]['weekends'] = weekend
    post_data(storedData)
    message = {
      'text': f'Ok, you {phraseyboi} study on weekends, what times do you want to study?',
      'author': 'Timetabler',
      'state': {'progress': 'times', 'author': author}
    }
    return jsonify(message)
  elif state['progress'] == 'times':
    author = state['author']
    storedData = get_data().json()
    data = request.get_json()
    times = data['text']
    times = times.split()
    if times[0][-2:] == 'am':
      time1 = int(times[0][0:-2])*100
    else:
      if int(times[0][0:-2]) != 12:
        time1 = int(times[0][0:-2])*100+1200
      else:
        time1 = 1200
    if times[2][-2:] == 'am':
      time2 = int(times[2][0:-2])*100
    else:
      if int(times[2][0:-2]) != 12:
        time2 = int(times[2][0:-2])*100+1200
      else:
        time2 = 1200
    if time2 <= time1:
      return jsonify({'text':'hey there fine human, it seems that you are trying to study past midnight, this is bad for your mental and physical health, so I am saying no.', 'state': {'progress': 'times', 'author': author}, 'author':'Timetabler'})
    storedData[author]['study'] = [time1, time2]
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