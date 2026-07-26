from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

model = ChatMistralAI(
    model_name = 'mistral-medium-latest'
)

parser = StrOutputParser()

code_prompt = ChatPromptTemplate.from_messages(
    [
        ('system', """You are a helpful AI assisstant, 
         who generates a python code on topic given by the user"""),
        ('human', 'Please generate the code of {topic}')
    ]
)

explain_prompt = ChatPromptTemplate.from_messages(
    [
        ('system', """You are a helpful AI assisstant, who explains the code given by the user. Do not include the introductory part."""),
        ('human', """{code}""")
    ]
)

seq = code_prompt | model | parser

chain = RunnableParallel(
    {
        'code': RunnablePassthrough(),
        'explain': explain_prompt | model | parser
    }
)

final_chain = seq | chain

topic = input("Enter topic :- ")
result = final_chain.invoke(
    {
        'topic': topic
    }
)

print(result['code'])
print()
print()
print(result['explain'])
