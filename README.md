#Trivi, a simple bot that seeks answer to trivia questions from the Internet

You can ask Trivi questions like
  "question": "A flashing red traffic light signifies that a driver should do what?",
  
Also prodive possible answers in multiple-choise format:
  "A": "stop",
  "B": "speed up",
  "C": "proceed with caution",
  "D": "honk the horn",

Current algrithom:
Trivi will search the question on google craw the google search page for keyword hits
Trivi will then search a correponded wikipedia article and craw for keyword hits

Hits from both sources are weighted and added to champion the right answer
Currently, trivi performs at 50% correct on the trivia dataset. Join me in the effort to make it better!
