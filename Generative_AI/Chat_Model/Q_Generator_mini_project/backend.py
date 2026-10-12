# Using structured outputs (JSON) and prompt templates to
# create a first mini-project of Gen AI
import os
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from fastapi import FastAPI, HTTPException
load_dotenv()


app = FastAPI(title = "Question Geenrator AI Chatbot")

class Para(BaseModel):

    introduction : str = Field(description = "The introductory part as confirming the number of questions generated that user entered")
    topic: Optional[str] = Field(description = "The topic of the given paragraph")
    questions: List[str]

parser = PydanticOutputParser(pydantic_object = Para)

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

class UserResponse(BaseModel):
    paragraph : str
    num_questions : int
    api_key: Optional[str] = None

@app.post('/')
def question_generator(response : UserResponse):

    if len(response.paragraph.split()) > 3000:
        raise HTTPException(
            status_code=422,
            detail="Input too long: Please limit your text to under 3,000 words."
        )

    api_key = (response.api_key or os.getenv("GROQ_API_KEY") or "").strip()
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="No Groq API key is configured. Set GROQ_API_KEY on the backend or provide a key in the UI."
        )

    try:
        model = ChatGroq(
            model="openai/gpt-oss-120b",
            temperature=0.35,
            api_key=api_key
        )
        prompt = prompt_template.invoke(
            {
                "num_questions": response.num_questions,
                "paragraph": response.paragraph,
                "format_instructions": parser.get_format_instructions()
            }
        )
        answer = model.invoke(prompt).content
        question_data = parser.parse(answer)
        return question_data.model_dump(mode="json")

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail="The model could not generate questions. Verify the Groq API key and check the backend logs."
        ) from error