"""
- provide tasks (incomplete)
- check answer correctness (probably needs refining)
- take input from the user and print outputs (check)
- communicate with assistant (needs assistant working for testing)
- operate task database (mocup)
"""
from assistant import Assistant

def load_tasks(file_name='tasks.json'):
    return []

def provide_task(tasks):
    return tasks[0]

def call_assitant() -> str:
    pass

def check_answer(task, answer:str) -> bool:
    if "".join(answer.split()) in task[2]:
        return True
    return False

# create assitant
assistant = Assistant('openai')
#ids of previous tasks
prev_tasks = []

#task: tuple (id, task_str, answers_str)
tasks = load_tasks()

#mocup
ex_task = (1, '2+2', ['4'])
tasks.append(ex_task)
quit = False
#prompt loop:
while not quit:
    answers = []
    task = provide_task(tasks)
    print('Try to solve the following task. If you need help type "help" or "h"')
    print(task[1])
    while True:
        answers.append(input('>>> '))
        #user wants help?
        if answers[-1] in ['q', 'quit']:
            quit = True
            break

        if answers[-1].lower() in ['h', 'help']:
            print(assistant.get_response(answers[-1], task, answers[0:-1]))
            answers.pop() #remove the query
            print('Try again!')
            break

        if check_answer(task, answers[-1]):
            print('Great job!')
            break
        print('Try again! Assistant will help you if you type "help" or "h"!')
    
print('bye bye!')