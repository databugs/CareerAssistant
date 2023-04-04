from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from pydantic import BaseModel, Field
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

class ProjectIdeas(BaseModel):
    project_ideas: list[str] = Field(description="List of project ideas.")

output_parser = PydanticOutputParser(pydantic_object=ProjectIdeas)

def custom_output_parser(llm_output: str):
    #logging.debug(f"LLM output: {llm_output}")
    if len(output_parser.parse(llm_output.replace("\n", "")).project_ideas)==5:
        return output_parser.parse(llm_output.replace("\n", "")).project_ideas
    ideas: ProjectIdeas = output_parser.parse(llm_output.replace('\n', ''))
    ideas_list = ideas.project_ideas[0]
    return [idea.strip() for idea in ideas_list.split(',')]

def clean_output(output):
        projects = output.strip()
        project_one = ''.join(
            project + '\n\n' for project in projects.split('\n\n')[:2][1].split('\n')[1:]
            )
        project_two = ''.join(
            project.strip() + '\n\n' for project in projects.split('\n\n')[2:][1].split('\n')[1:]
            )
        title_one = projects.split('\n\n')[:2][0]
        title_two = projects.split('\n\n')[2:][0]
        project1 = ''.join(item +'\n\n' for item in [f'*{title_one}*', project_one])
        project2 = ''.join(item +'\n\n' for item in [f'*{title_two}*', project_two])
        return [project1.strip(), project2.strip()]

def setup(job=None, level=None, industry=None):
    def setup(job=None, level=None, industry=None):
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    #output_parser = PydanticOutputParser(pydantic_object=ProjectIdeas)

    format_instructions = output_parser.get_format_instructions()

    template = """
    You are The Data Alchemist, a bot for a career growth and acceleration website.
    Your job is to generate a list of recommended projects that will lead to career growth,
    given a job title, Level, and Industry of the use case.
    
    Output Format:
    1. Project 1
    2. Project 2
    3. Project 3,
    4. Project 4,
    5. Project 5.

    {format_instructions}

    INPUT:
    List 5 recommended projects for {job_title}, {level}, {industry}.

    YOUR RESPONSE:
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=["job_title", "level", "industry"],
        partial_variables={"format_instructions": format_instructions}
    )

    model = OpenAI(temperature=0.7)

    _input = prompt.format(job_title=job, level=level, industry=industry)
    return model(_input)
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=["job", "level", "industry"]
    )

    #logging.debug(f"Input variables: job_title={job}, level={level}, industry={industry}")

    model = OpenAI(temperature=0.7, openai_api_key=OPENAI_API_KEY, max_tokens=1004)

    _input = prompt.format(job=job, level=level, industry=industry)

    return model(_input)
