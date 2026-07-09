# Using structured outputs (JSON) and prompt templates to
# create a first mini-project of Gen AI

from langchain_mistralai import ChatMistralAI
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

class Essay(BaseModel):

    introduction : str = Field(description = "The introductory part as confirming the number of questions generated that user entered")
    topic: Optional[str] = Field(description = "The topic of the given paragraph")
    questions: List[str]

parser = PydanticOutputParser(pydantic_object = Essay)

prompt_template = ChatPromptTemplate.from_messages([
    (
        'system',
        """
You are an expert educational assessment engine. Your task is to analyze the
provided paragraph and generate a series of high-quality, conceptual, and
accurate questions based strictly on the text. Do not include the concluding text—output only the questions.
The format must be {format_instructions}.
"""
    ),
    (
        'human',
        """
Generate exactly {num_questions} questions from the following paragraph:

{paragraph}
"""
    )
])

def question_generator(paragraph : str, num_q : int, api_key: str) -> str:

    if len(paragraph.split()) > 3000:
        raise ValueError("Input too long: To keep our free API tiers healthy, please limit your text to under 5,000 words.")
    else:
        try:
            model = ChatMistralAI(
                    model = "mistral-medium-latest",
                    temperature = 0.35,
                    api_key = api_key
            )
            prompt = prompt_template.invoke(
                {
                    "num_questions" : num_q,
                    "paragraph" : paragraph,
                    "format_instructions" : parser.get_format_instructions()
                }
            )
            response = model.invoke(prompt).content
            question_data = parser.parse(response)
            output = question_data.model_dump_json(indent = 2)

            return output
        except Exception as error:
            return f"The model cannot load the questions at the moment as {error}"