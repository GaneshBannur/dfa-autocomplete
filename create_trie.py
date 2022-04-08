#building a trie from the word corpus in words.txt
from anytree import Node

def traverse_and_add(prefix, root):
  current=root
  for letter in prefix:
    flag=0
    for child in current.children:
      if letter==child.name:
        current=child
        flag=1
        break
    if flag!=1:
      temp = Node(letter, parent=current, accepting=0)
      current = temp
  current.accepting = 1

root = Node ('0', accepting=0)
fhand=open('./words.txt')
for word in fhand:
  if word[-1]=="\n":
    word = word[:-1]
  if len(word)>1:
    traverse_and_add(word,root)

#conversion of the trie to a dfa and storing it in a txt file for minimization

states = {root:"q0"}
alphabet = set(())
accepting_states = set(())
transition_function = {}

def traverse(root, node_num):
  current = root
  transition_function[states[current]] = {}
  if current.accepting==1:
    accepting_states.add(states[root])
  for child in current.children:
    node_num += 1
    states[child] = "q"+str(node_num)
    alphabet.add(child.name)
    transition_function[states[current]][child.name] = states[child]
    node_num = traverse(child, node_num)
  return node_num

traverse(root, 0)

dfa_file = open(file = r"initial_dfa.txt", mode = 'w')
for key in list(states)[:-1]:
  dfa_file.writelines(states[key]+",")
dfa_file.writelines(states[list(states)[-1]]+"\n")
for letter in list(alphabet)[:-1]:
  dfa_file.writelines(letter+",")
dfa_file.writelines(list(alphabet)[-1]+"\n")
dfa_file.writelines("q0")
dfa_file.write("\n")
for state in list(accepting_states)[:-1]:
  dfa_file.writelines(state+",")
dfa_file.writelines(list(accepting_states)[-1]+"\n")
for node in transition_function:
  for input in transition_function[node]:
    dfa_file.write(node+","+input+"=>"+transition_function[node][input]+"\n")

dfa_file.close()