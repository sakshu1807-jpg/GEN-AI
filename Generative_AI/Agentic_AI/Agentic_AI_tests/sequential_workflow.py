from langchain_mistralai import ChatMistralAI
from typing import TypedDict, Dict
from langgraph.graph import StateGraph
from dotenv import load_dotenv
load_dotenv()

"""
Workflow :-
1. Raw paragraph in English
2. Grammatical Mistakes
3. Converting to Hindi
4. Output
"""

# Creating State
class Sequential_State(TypedDict):
    raw_para : str
    edited_para : str
    translated_para : str

model = ChatMistralAI(
    model_name= "mistral-medium-latest",
    temperature= 0.5
)

def para_editor(state: Sequential_State) -> Dict:
    prompt = f"""
            Please fix all grammar, spelling, and punctuation errors in the paragraph below. 
            Keep the original meaning and tone the same. Do not add any extra information or change the style more than needed. 
            Just output the final edited paragraph.
            Input paragraph: {state['raw_para']}
            """
    result = model.invoke(prompt)
    return {
        "edited_para": result.content
    }

def para_transltor(state: Sequential_State) -> Dict:
    prompt = f"""
            Translate the paragraph below into natural, accurate Hindi. 
            Provide only the final translated Hindi text. Do not include any English explanation, notes, or introductory text.
            Input Paragraph: {state['edited_para']}
            """
    result = model.invoke(prompt)
    return {
        "translated_para": result.content.strip()
    }

# Creating the LangGraph state
graph = StateGraph(Sequential_State)

# Adding the nodes / tasks to the graph
graph.add_node("editor", para_editor)
graph.add_node("translator", para_transltor)

# Adding the edges / connecting lines to the graph
from langgraph.graph import START, END
graph.add_edge(START, 'editor')
graph.add_edge('editor', 'translator')
graph.add_edge('translator', END)

# Compiling all the nodes and edges to the final var
app = graph.compile() # Now, this also became a runnable

paragraph = """yesterday i went to the market for buying some fresh fruits but it started raining heavily and 
i forgot my umbrella at home? i ran inside a small coffee shop to save myself from getting wet, 
everyone inside was drinking hot tea and eating snacks. the shopkeeper was very friendly 
he gave me a dry towel to wipe my face! even though i could not buy the fruits, i still had a good time because 
i met a old friend there after many years.
"""

final_result = app.invoke({
    "raw_para": paragraph
})

print(final_result['edited_para'])
print('\n\n')
print(final_result['translated_para'])