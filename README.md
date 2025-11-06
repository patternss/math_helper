# math_helper
LLM based math helper that supports the student with math tasks. 

## functionality: 
- takes input from the user 
- uses current student tasks and previous answers as part of its context
- can call a calculator app to ensure the right answer
- use of openAI's API
  - optionally uses local model via ollama
- brief pedagogic prompting
- brief security & safety guardail promp


### example use case:
student has a problem in their math quiz app. 
--> they answer couple of times and get wrong answers
--> they ask help from the math helper: -I'm getting wrong
    answers, can you help me with this?
--> math creates a hint based on the current task and previous answers
--> students tries again, with the helpful message and gets the correct
    answer