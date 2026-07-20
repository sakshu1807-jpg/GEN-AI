from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

model = ChatMistralAI(
    model = 'mistral-medium-latest',
    temperature = 0.5
)

short_prompt = ChatPromptTemplate.from_template(
    'Please explain {topic} in 30-40 words.'
)

detailed_prompt = ChatPromptTemplate.from_template(
    'Please explain {topic} in detail.'
)

str_parser = StrOutputParser()

runnable_parallel = RunnableParallel(
    {
        "short": RunnableLambda(lambda x : x['short']) | short_prompt | model | str_parser,
        "detailed": RunnableLambda(lambda x : x['detail']) | detailed_prompt | model | str_parser
    }
)

result = runnable_parallel.invoke(
    {
        'short': {'topic': 'Machine Learning'},
        'detail': {'topic': 'Deep Learning'}
    }
)

print(result['detail'])