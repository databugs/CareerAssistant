from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from pydantic import BaseModel, Field
import os
#import logging

# Set up logging
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

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

def setup(job=None, level=None, industry=None):
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    #logging.debug(f"OPENAI_API_KEY: {OPENAI_API_KEY is None}")

    format_instructions = output_parser.get_format_instructions()

    template = """
    You are an AI-based career coach tasked with generating practical and achievable 
    recommendations for two innovative projects that can lead to career growth based 
    on a job title, level, and industry. For each project, provide 3-5 specific and 
    actionable steps that the individual can take.

    Input Format:
    {Job_title}
    {Level}
    {Industry}

    Output Format:

    Project 1: [Give the project a title]

    Action Points
    1. [Description of first actionable step]
    2. [Description of second actionable step]
    3. [Description of third actionable step]
    [Additional action points if needed]

    Project 2: [Give the project a title]

    Action Points
    1. [Description of first actionable step]
    2. [Description of second actionable step]
    3. [Description of third actionable step]
    [Additional action points if needed]

    Instructions:
    Provide two innovative yet practical project recommendations tailored to the given job 
    title, level, and industry that can help the individual achieve career growth. For each project, 
    specify 3-5 clear and actionable steps that the person can take to complete the project. 
    The recommendations and action points should be realistic and achievable based on the 
    individual's position and experience. Ensure that all action points are phrased as 
    guided steps (e.g. "Reach out to your manager to discuss taking on more responsibility" 
    vs. "Getting more responsibility"). The most important criteria are practicality and 
    achievability, as well as specificity and clarity.
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=["job_title", "level", "industry"]
    )

    #logging.debug(f"Input variables: job_title={job}, level={level}, industry={industry}")

    model = OpenAI(temperature=0.7, openai_api_key=OPENAI_API_KEY)

    _input = prompt.format(job_title=job, level=level, industry=industry)

    return model(_input)
