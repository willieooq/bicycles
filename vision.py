#!/usr/bin/python3
# coding=utf8

import io
import json
import os
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
  'spoke', 'bicycle saddle', 'bicycle fork', 'bicycle drivetrain part'
]

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

  for label in labels:
    description =  label.description.lower()
    print('Processing label:', description)
    if description in bike_labels:
      print('{} in'.format(description))
      ret[description] = label.score
    else:
      print('{} not in'.format(description))
  return ret

# function call here

# image_labels = detect_labels(path)
# scores = get_bike_scores(image_labels)
# print('final score:', scores)
