import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()
prompt_template = """
Prompt:
Organize and summarize the JSON data below in a structured Markdown format. 

The JSON data follows this structure:
```
{{
    "Data": [
        {{
            "type": "url",
            "position": "URL",
            "title": "Title of the URL",
            "content": "Content of the URL",
            "index": 0
        }}
    ],
    "length": 1
}}
```

**Instructions for summarization**:
1. **Categorize URLs**: Group the URLs based on the "type" attribute or other meaningful properties (like topics, sources, etc.).
2. **List Categories**: At the top of the summary, provide a categorized list of URLs by their titles, linking to each summary.
3. **Summarize by Category**: Under each category, provide a concise summary of each URL's content in markdown format.

**Example format for output**:

```
# Summary by Category

## Category 1: [e.g., "News Articles"]
- [Title of URL 1](#title-of-url-1)
- [Title of URL 2](#title-of-url-2)

## Category 2: [e.g., "Research Papers"]
- [Title of URL 3](#title-of-url-3)

---

# Detailed Summaries

## Category 1: News Articles

### Title of URL 1
Summary of content...

### Title of URL 2
Summary of content...

## Category 2: Research Papers

### Title of URL 3
Summary of content...
```

Below is the JSON data for summarization:
{json_data}
"""

def list_model() :
    for model in genai.list_models():
        print(model)
    # current using model = 'models/gemini-1.5-flash-8b-latest',
def debug_and_verbose():
    from langchain.globals import set_verbose, set_debug
    set_debug(True)
    set_verbose(True)
def summaryJson(jsonData) : 
    prompt = PromptTemplate(input_variables=["json_data"], template=prompt_template)
    llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash-8b-latest')
    chain = prompt | llm
    response = chain.invoke({"json_data": jsonData})
    return { "response": response.content, "metadata": response.usage_metadata }

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