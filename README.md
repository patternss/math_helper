# math_helper
LLM based math helper that supports the student with math tasks. 

## functionality: 
- provide the user with math tasks and check the answer
- process user input - if user asks for help, create a helpful answer
- uses current student tasks and previous answers as part of its context
- help is provided stepwise (no giving up the answer at first try)
- offers different LLM-setups


### example usecase:
student has a problem in their math quiz app. 
--> they answer couple of times and get wrong answers
--> they ask help from the math helper: -I'm getting wrong
    answers, can you help me with this?
--> math creates a hint based on the current task and previous answers
--> students tries again, with the helpful message and gets the correct
    answer

### Parts of the program:

#### math_app
- provide tasks
- check answer correctness
- take input from the user and print outputs
- communicate with assistant
- operate task database

#### assistant
- create responses for queries
- LLM setup
- store chat history
- store pedagogic prompt
- communicate with calculator if needed

#### task_database
- store question - answer pairs
- hold statistics?

#### calculator
- solve math problems stepwise and return steps 

#### RAG-database
- store educational and informational math documents
- initialize vecotor store
- provide documents based on queries