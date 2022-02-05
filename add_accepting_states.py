import json

#load minimized dfa from JSON file
with open('minimized_dfa.json', 'r') as fp:
    minimized_dfa = json.load(fp)

root = 'q0'
final_dfa = {}
final_dfa[root] = {"accepting":0, "transitions":minimized_dfa[root]}

def traverse(prefix):
  current = root
  for idx, letter in enumerate(prefix, start=1) :
    for transition in minimized_dfa[current] :
      if letter==transition :
        current=minimized_dfa[current][transition]
        if current not in final_dfa:
          if idx==len(prefix):
            final_dfa[current] = {"accepting":1, "transitions":minimized_dfa[current]}
          else:
            final_dfa[current] = {"accepting":0, "transitions":minimized_dfa[current]}
        break

fhand=open('./words.txt')
for word in fhand:
  word = word[:-1]
  traverse(word)

with open('minimized_dfa_with_accepting.json', 'w') as fp:
    json.dump(final_dfa, fp)