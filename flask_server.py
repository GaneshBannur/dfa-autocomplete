"""creates a flask server which runs the method to autocomplete a word on the request of the
script running on the text editor"""

from flask import Flask, request
from flask_cors import CORS
import json

with open('minimized_dfa_with_accepting.json', 'r') as fp:
    final_dfa = json.load(fp)
root = 'q0'

app = Flask(__name__)
CORS(app)

def traverse_and_find(root, prefix):
  current = root
  for letter in prefix :
    flag=0
    for transition in final_dfa[current]["transitions"] :
      if letter==transition :
        current=final_dfa[current]["transitions"][transition]
        flag=1
        break
    if flag!=1 :
      return '\0'
  return_str=""
  while(len(final_dfa[current]["transitions"])>0):
    next_node = next(iter(final_dfa[current]["transitions"]))
    return_str += next_node
    current = final_dfa[current]["transitions"][next_node]
    if final_dfa[current]["accepting"]==1:
      return return_str
  return return_str

@app.route('/', methods=['POST', 'GET'])
def autocorrect():
    if request.method == 'POST':
        return traverse_and_find(root, next(iter(request.form)))
    else:
        return "Failure"

app.run()