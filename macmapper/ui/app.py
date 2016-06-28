#!/usr/bin/env python3
import os
from flask import Flask, jsonify, send_from_directory

app = Flask(__name__)

@app.route('/static/<path:path>', methods=['GET'])
def get_static(path):
  cur_dir = os.path.dirname(os.path.abspath(__file__))
  return send_from_directory(os.path.join(cur_dir, 'static'), path)

@app.route('/', methods=['GET'])
def get_index():
  cur_dir = os.path.dirname(os.path.abspath(__file__))
  return send_from_directory(cur_dir, 'index.html')

@app.route('/api/devices', methods=['GET'])
def get_devices():
  return jsonify({'devices': []})

def run():
  app.run(debug=True)

if __name__ == '__main__':
  run()
