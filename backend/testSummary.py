from dotenv import load_dotenv
from langchain.globals import set_verbose, set_debug

set_debug(True)
set_verbose(True)
load_dotenv()

import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

def list_model() :
    for model in genai.list_models():
        print(model)

#'models/gemini-1.5-flash-8b-latest',

prompt_template = """
Summarize the following json data in a concise, and  md format
the json data format is 
json_data = {{ "Data": [ {{ "type": "url",
            "position": "URL",
            "title": "Title of the URL",
            "content": "Content of the URL"
            "index": 0
        }},
    ],
    "length": 1
}}
and you need to summarize the content of the URL and write it in a markdown format
below is the json data:
{json_data}
"""
import json
with open("./UserData/test_user/10-30.diary") as f:
    json_data = json.load(f)

prompt = PromptTemplate(input_variables=["json_data"], template=prompt_template)
llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash-8b-latest')
chain = prompt | llm
response = chain.invoke({"json_data": json_data})
print(response)

"""
content='I am doing well, thank you for asking.  How are you?\n'
 additional_kwargs={} 
 response_metadata={'prompt_feedback': 
 {'block_reason': 0, 'safety_ratings': []}, 
 'finish_reason': 'STOP', 
 'safety_ratings': [{'category': 'HARM_CATEGORY_HATE_SPEECH', 'probability': 'NEGLIGIBLE', 'blocked': False}, 
 {'category': 'HARM_CATEGORY_DANGEROUS_CONTENT', 'probability': 'NEGLIGIBLE', 'blocked': False}, 
 {'category': 'HARM_CATEGORY_HARASSMENT', 'probability': 'NEGLIGIBLE', 'blocked': False}, 
 {'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT', 'probability': 'NEGLIGIBLE', 'blocked': False}]} 
 id='run-71b42269-b560-4276-98ca-bccfeb6bd8c4-0' 
 usage_metadata={'input_tokens': 7, 'output_tokens': 16, 'total_tokens': 23, 'input_token_details': {'cache_read': 0}}
"""