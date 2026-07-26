from langchain.tools import tool
from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser
from rich import print
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
load_dotenv()

messages = []

# 1. Tool Creation

@tool
def get_text_length(text: str) -> int:
    """This function returns the length of the text given"""
    return len(text)

@tool
def uppercase_text(text: str) -> str:
    """This function returns the uppercase form of the text given"""
    return text.upper()

tools = {
    'get_text_length': get_text_length,
    'uppercase_text': uppercase_text
}
# 2. Tool Binding

model = ChatMistralAI(
    model_name = 'mistral-medium-latest'
)
parser = StrOutputParser()

model_with_tools = model.bind_tools([get_text_length, uppercase_text])

string = input("Enter the string :- ")
task = input("Enter tool task (uppercase/ length) of text) :- ")

if task.strip().lower() == 'uppercase':
    prompt = f"I want to convert all the text to uppercase. The text is {string}"

else:
    prompt = f"Tell me number of characters present in the string. The string is {string}"

messages.append(HumanMessage(prompt))

result = model_with_tools.invoke(messages)
messages.append(result) # Tools selected by model included (Not used AIMessage bcuz we don't only want content but whole result)

# 3. Tool Selection by model

for tool_call in result.tool_calls:
    print("Tool suggested is :- ", tool_call.get('name'))
    print()
    print("The args is :- ", tool_call.get('args'))

# 4. Tool Execution

if not result.tool_calls:
    print("No tools found to use.")

else:
    for tool_call in result.tool_calls:
        tool_name = tool_call['name']
        selected_tool = tools[tool_name]

        tool_result = selected_tool.invoke(tool_call)
        messages.append(tool_result)

final_result = model_with_tools.invoke(messages)
answer = parser.parse(final_result.content)
print(answer)
