import requests
import json
import random
import base64


# TODO: add score mechanism
# clear screen after each question

categories = {
  "A": 14,
  "B": 18,
  "C": 24,
  "D": 11,
  "E": 20,
  "F": 12
}

trivia_options = """ Trivia Options: 
A. Television

B. Computer Science

C. Politics

D. Movies

E. Mythology

F. Music

G. Random

H. Any

"""

categories["G"] = random.randint(9, 32)

print(trivia_options)

category=input(" Select a category ").upper()
category_string = "&category="

while category not in categories.keys() and category != "H":
  category=input(" Select a CATEGORY! ").upper()

if category == "H":
  category_string = ""
else:
  category_string += str(categories[category])


print("""
Difficulty Options: 

A: Easy

B: Medium

C: Hard

D: Random

E: Any

""")

difficulties = {
  "A": "easy",
  "B": "medium",
  "C": "hard",
}
difficulties["D"] = random.choice(["easy", "medium", "hard"])

difficulty=input( "Select a difficulty letter: ").upper()
difficulty_str = "&difficulty="
while difficulty not in difficulties.keys() and difficulty != "E":
  difficulty=input(" Select a DIFFICULTY! ").upper()

if difficulty == "E":
  difficulty_str = ""
else:
  difficulty_str += str(difficulties[difficulty])

url = f"https://opentdb.com/api.php?amount=10{category_string}&type=multiple&encode=base64"

questions = requests.get(url).json()["results"]

for question in questions:
  print(base64.b64decode(question["question"]).decode('utf-8'))

  possible_answers=question["incorrect_answers"]
  possible_answers.append(question["correct_answer"])
  random.shuffle(possible_answers)

  answer_dict = {}
  letters = ["D","C","B","A"]
  for answer in possible_answers:
    letter = letters.pop()
    answer_dict[letter] = answer
    print(f"{letter}. {base64.b64decode(answer).decode('utf-8')}")

  # print(f"Correct answer: {question['correct_answer']}")
  print("")
  # ask to select an answer
  
  user_letter=input("  Select your answer:  ").upper()

  while user_letter not in answer_dict.keys():
    print("This isn't an answer. Pick one from the list of answers.")
    user_letter=input("  Select your answer:  ").upper()

  user_answer = answer_dict[user_letter]


  if user_answer==question["correct_answer"]:
    print(" Correct! ")
  else:
    print(" Incorrect. ")
  print("")



