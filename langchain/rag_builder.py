from openai import AzureOpenAI
import os
from dotenv import load_dotenv

EVALUATION_PROMPT = "whats the capital in china?"

class API_CLIENT():
  def __init__(self):
    #Sets the current working directory to be the same as the file.
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    #Load environment file for secrets.


    #Create Azure client
    self.client = AzureOpenAI(
        api_key='bc66fc90cd3448e68de391ea7e0074f0',
        api_version='2024-06-01',
        azure_endpoint = 'https://api.umgpt.umich.edu/azure-openai-api',
        organization = "016732"
    )
    self.model = 'gpt-4o'

  def send_query(self, inputPrompt, userAnswer, correctAnswer):
   # Format the prompt with the given instruction, response, and reference answer
    prompt = EVALUATION_PROMPT.format(
        instruction=inputPrompt,
        response=userAnswer,
        reference_answer=correctAnswer
    )

    #Create Query
    messages=[
            {"role": "system","content": "You are a fair evaluator language model"},
            {"role": "user","content": prompt},
        ]

    # Send a completion request.
    response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0,
            stop=None)

    #Print response.
    return response.choices[0].message.content

client = API_CLIENT()
print(client.send_query("11","beijing","hhh"))