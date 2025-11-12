"""
 create responses for queries
- LLM setup
- store chat history
- store pedagogic prompt
- communicate with calculator if needed
"""

from openai import OpenAI

class Assistant():
    def __init__(self, llm_tool :str ="openai" ):
        self.llm_tool = llm_tool
        self.msg_history = {}

        #initialize the chosen llm_tool
        match llm_tool:
            case "openai":
                self.client = OpenAI()
            case "ollama" :
                pass
            case _ :
                print('unknown llm tool provided') 

        #load pedagogic prompt
        with open('pedagogic_prompt.md', 'r') as file:
            self.peda_prompt = " ".join(line.rstrip() for line in file)
        

    
    
    def get_response(self, query, context):
        """
        fetches/creates an response based on the query and context. 
        context includes the student's past answers and the task
        """
        if self.llm_tool == 'openai':
            
            client = self.client

            response = client.responses.create(
                model="gpt-5",
                input="tehtävä: 2*(5-3)+12, opiskelijan viesti: Olen täysin jumissa!" \
                "En tiedä mistä lähteä liikkeelle! Apua!",
                instructions="olet matematiikka-apuri. Nimesi on Lennart. Tehtäväsi on " \
                "auttaa oppilasta, pitämällä kuitenkin oppiminen hauskana. " \
                "Käytä seuraavanlaista lähestymistapaa vastauksen luomisessa:" \
                "1. Aloita vastaus kevyellä vitsillä. " \
                "2. Ratkaise annettu tehtävä ja palauta kaikki ratkaisuvaiheet " \
                "seuraavassa muodossa: 1. '1. askel' \n 2. 'toinen askel' ... " \
                "n. 'n askel. " \
                "3. Kerro loppuvitsi. " \
                "4. Kerro vastauksesi tyylillä, jossa mainitset oman nimesi aina " \
                "esim. Lennartin mielestä, nyt ei tarvitse hätäillä." 
            )
            return response.output_text





if __name__ == '__main__':
    print('__main__')