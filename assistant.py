"""
 create responses for queries
- LLM setup
- store chat history
- store pedagogic prompt
- communicate with calculator if needed
"""

from pathlib import Path
from openai import OpenAI
from ollama import chat
import re

class Assistant():
    def __init__(self, llm_tool :str ="openai", model_name=None ):
        self.llm_tool = llm_tool
        self.msg_history = []
        self.model_name = model_name

        #initialize the chosen llm_tool
        match llm_tool:
            case "openai":
                self.client = OpenAI()
                #check if model was set - use default if not
                if not self.model_name:
                    self.model_name = "gpt-5"

            case "ollama" :
                #check if model was set - use default if not
                if not self.model_name:
                    self.model_name = "deepseek-r1:1.5b"
                
            case _ :
                print('unknown llm tool provided - initialization failed.') 

        #load pedagogic prompt
        BASE_DIR = Path(__file__).resolve().parent
        file_path = BASE_DIR / "pedagogic_prompt.md"
        with open(file_path, 'r') as file:
            self.pedag_prompt = " ".join(line.rstrip() for line in file)
        

    
    def clear_msg_history(self):
        self.msg_history = []

    def create_extended_query(self, help_msg, task, answers):
        """combines query and context into one message that is processable 
        by the LLM"""
        ext_query = []
        prev_answ_str = "\n".join([f'{i}:{answ}' for i, answ in enumerate(answers, start=1)])
        
        #add combined system prompt (pedagogic prompt, task and previous answers)
        complete_system_prompt = f'{self.pedag_prompt} \
                          \n\nThe current task is {task[1]} with the correct \
                          answer of {task[2]}\n\nand these \
                          are the previous answers the student has tried:\n\n\
                          {prev_answ_str}'
        
        ext_query.append({'role':'system', 'content': complete_system_prompt })
        
        ext_query.extend(self.msg_history)
        ext_query.append({'role':'user', 'content': help_msg})

        return ext_query


    def get_response_openai_(self, extened_query):
        """
        fetches/creates an response based on the query and context. 
        context includes the student's past answers, problem description, 
        and message history and the pedagogic prompt.
        """
    
        
        client = self.client

        response = client.responses.create(
            model=self.model_name,
            input=extened_query
            )
        return response.output_text

    def get_response_ollama_(self, extended_query):
        """
        fetches/creates an response based on the query and context. 
        context includes the student's past answers, problem description, 
        and message history and the pedagogic prompt.
        """

        #query the model
        response = chat(model=self.model_name, messages = extended_query)
        message = re.sub(r'<think>.*</think>',"",response.message.content, flags=re.DOTALL)
        return message    
    def get_response(self, help_msg:str, task:str, answers):
        
        extended_query = self.create_extended_query(help_msg, task, answers)
        match self.llm_tool:
            case 'openai':
                assistant_answer = self.get_response_openai_(extended_query)
            case 'ollama':
                assistant_answer = self.get_response_ollama_(extended_query)
            case _ : "couldn't create a response, no llm tool initialized!"

        #update message history:
        self.msg_history.extend([{'role':'user', 'content':'help_msg'}, \
                                {'role':'assistant', 'content':assistant_answer}])
        
        return assistant_answer

    




if __name__ == '__main__':
    print('you ran assistant.py as __main__')