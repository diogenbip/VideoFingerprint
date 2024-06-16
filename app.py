import os
from flask import Flask, render_template, request
import libs.ContentDataSet as CDS
from libs.Lsh import LSH

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

audioLSH = LSH(threshold=0.79)
videoLSH = LSH(threshold=0.79)

@app.route('/upload', methods=['POST'])
def upload():
  if 'video' not in request.files:
    return 'No video uploaded', 400
  file = request.files['video']
  
  if file: 
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  return 'ok'

@app.route('/init', methods=['GET'])
def init():
  dataset = CDS.ContentDataset('static/init')
  audio = dataset.content_list[0][1]
  video = dataset.content_list[0][2]
  for i,a in enumerate(audio[:-1]):
    audioLSH.search(a, dataset.content_list[0][0], i)
  for i,v in enumerate(video[:-1]):
    videoLSH.search(v, dataset.content_list[0][0], i)
  return 'ok'
  
  
@app.route('/fingerprint', methods=['GET'])
def fingerprint():
  id = request.args.get('id')
  fingerprints = CDS.process_video(id, app.config['UPLOAD_FOLDER'])
  audio = fingerprints[1]
  video = fingerprints[2]
  for i,a in enumerate(audio[:-1]):
    audioLSH.add(a, id, i)
  for i,v in enumerate(video[:-1]):
    videoLSH.add(v, id, i)
  return 'ok'


@app.route('/search', methods=['GET'])
def search():
  id = request.args.get('id')
  if id:
    fingerprints = CDS.process_video(id, app.config['UPLOAD_FOLDER'])
    audio = fingerprints[1]
    video = fingerprints[2]
    a_ress = {}
    v_ress = {}
    for i,a in enumerate(audio[:-1]):
      res = audioLSH.search(a, id, i,  add_to_bucket = False)
      if res != None:
        if res[1] not in a_ress:
          a_ress[res[1]] = []
        a_ress[res[1]].append(((i*1.48)/60,(res[2]*1.48)/60,res[3]))
    for i,v in enumerate(video[:-1]):
      res = videoLSH.search(v, id, i,  add_to_bucket = False)
      if res != None:
        if res[1] not in v_ress:
          v_ress[res[1]] = []
        v_ress[res[1]].append(((i*2)/60,(res[2]*2)/60,res[3]))
  return {
    'audio': a_ress,
    'video': v_ress
  }

@app.route('/')
def index():
  return "ok"