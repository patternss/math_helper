"""
 create responses for queries
- LLM setup
- store chat history
- store pedagogic prompt
- communicate with calculator if needed
"""

from pathlib import Path
from openai import OpenAI

class Assistant():
    def __init__(self, llm_tool :str ="openai" ):
        self.llm_tool = llm_tool
        self.msg_history = []

        #initialize the chosen llm_tool
        match llm_tool:
            case "openai":
                self.client = OpenAI()
            case "ollama" :
                pass
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
        ext_query.append({'role':'system', 'content': self.pedag_prompt + \
                          '\nThe current task is ' + task + '\nand these '
                          'are the previous answers the student has tried:\n' + \
                          prev_answ_str})
        
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
            model="gpt-5",
            input=extened_query
            )
        return response.output_text

    def get_response_ollama_(self, query, context):
        pass

    def get_response(self, help_msg:str, task:str, answers):
        
        extended_query = self.create_extended_query(help_msg, task, answers)
        match self.llm_tool:
            case 'openai':
                assistant_answer = self.get_response_openai_(extended_query)
            case 'ollama':
                pass
            case _ : "couldn't create a response, no llm tool initialized!"

        #update message history:
        self.msg_history.extend([{'role':'user', 'content':'help_msg'}, \
                                {'role':'assistant', 'content':assistant_answer}])
        
        return assistant_answer

    




if __name__ == '__main__':
    print('you ran assistant.py as __main__')