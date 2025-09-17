import streamlit as st
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


import os 
from dotenv import load_dotenv
load_dotenv()

##Implemnting Langsmith Tracking
os.environ['LANGCHAIN_API_KEY'] =  os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Q&A Chatbot with Genai"


#defing the prompt template
prompt =  ChatPromptTemplate.from_messages(
    [
        ("system", "You are an helpful assistants. Please response to the user queries"),
        ("user", "Question:{question}")
    ]
)


def generate_response(question, api_key, llm, temperature, max_tokens):
    os.environ["GOOGLE_API_KEY"] = api_key
    llm = ChatGoogleGenerativeAI(model=llm)
    output_parser =  StrOutputParser()
    chain = prompt|llm|output_parser
    answer = chain.invoke({'question':question})
    return answer


##building an streamlit app
st.title("Q&A Chatbot with Google Genai")

#sidebar
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter yout Google_Genai API key:", type="password")

#drop to select various models
llm = st.sidebar.selectbox("Select An Genai model", ["gemini-2.0-flash-exp", "gemini-1.5-flash", "gemini-1.5-pro"])

#adjusting the response parameter
temperature  = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)


## Main interface for user input
st.write("Go ahead and you can ask any question")
user_input = st.text_input("You:")

if user_input:
    response = generate_response(user_input, api_key, llm, temperature, max_tokens)
    st.write(response)
else:
    st.write("Please Provide the Query")
