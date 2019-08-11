#!/usr/bin/python3
# coding=utf8

import io
import json
import os
from bike_predict import *
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
gac_path = os.path.join(
  os.path.dirname(__file__),
  'secrect_key',
  'Bicycles-vision.json'
)
print('gac: ' + gac_path)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = gac_path
bike_labels = [
  'bicycle', 'bicycle wheel', 'bicycle part', 'bicycle frame', 'bicycle tire', 'vehicle',
  'spoke', 'bicycle saddle', 'bicycle fork', 'bicycle drivetrain part', 'wheel'
]
path = os.path.join(
        os.path.dirname(__file__),
        'resources',
        'bike_07.jpg')
# Instantiates a client
client = vision.ImageAnnotatorClient()

def detect_text(path):
  print('detect_text() started with path:', path)

  with io.open(path, 'rb') as image_file:
      content = image_file.read()
  # print('content', content)

  print('Before parse image.')
  image = types.Image(content=content)
  # print('image:', image)

  # difference here
  response = client.text_detection(image=image)
  print('response:', response)
  texts = response.text_annotations
  print('Texts:')

  for text in texts:
    print('描述:', text.description)
    # end of detect_text

# Detects labels in the file
def detect_labels(path):
  print('detect_labels() started.')

  with io.open(path, 'rb') as image_file:
      content = image_file.read()

  image = types.Image(content=content)

  response = client.label_detection(image=image)
  labels = response.label_annotations
  print('detect_labels() label results:', labels)
  return labels
  # end of detect_labels()

def get_bike_scores(labels):
  print('labels length:', len(labels))
  ret = dict()
  possibility = 0
  sum_score = 0
  for label in labels:
    description =  label.description.lower()
    print('Processing label:', description)
    if description in bike_labels:
      print('{} in'.format(description))
      print(label.score)
      ret[description] = label.score
      possibility = possibility+1
      sum_score = sum_score+label.score
    else:
      print('{} not in'.format(description))
  return possibility, sum_score
  # return ret

##function call here
# scores = {
#   'bicycle':'0',
#   ' bicycle_wheel':'0',
#    'bicycle_part':'0', 
#    'bicycle_frame':'0', 
#    'bicycle_tire':'0', 
#    'vehicle, spoke':'0', 
#    'bicycle_saddle':'0', 
#    'bicycle_fork':'0', 
#    'bicycle_drivetrain_part':'0'
# }

# image_labels = detect_labels(path)
# scores = get_bike_scores(image_labels)
# print('final score:', scores,'\n')

# keras_bike_predict(float(scores['bicycle']), float(scores['bicycle_wheel']),\
#    float(scores['bicycle_part']), float(scores['bicycle_frame']), float(scores['bicycle_tire']),\
#    float(scores['vehicle']), float(scores['spoke']), float(scores['bicycle_saddle']), \
#    float(scores['bicycle_fork']),float(scores[' bicycle_drivetrain_part']))
