from crewai import Agent
from dotenv import load_dotenv

from agents_rag.tools import tool

load_dotenv()
import os

from langchain_google_genai import ChatGoogleGenerativeAI

## call the gemini models
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GEMINI_API_KEY"),
)

# Creating a senior researcher agent with memory and verbose mode

news_researcher = Agent(
    role="Senior Researcher",
    goal="Unccover ground breaking technologies in {topic}",
    verbose=True,
    memory=True,
    backstory=(
        "Driven by curiosity, you're at the forefront of"
        "innovation, eager to explore and share knowledge that could change"
        "the world."
    ),
    tools=[tool],
    llm=llm,
    allow_delegation=True,
)

## creating a write agent with custom tools responsible in writing news blog

news_writer = Agent(
    role="Writer",
    goal="Narrate compelling tech stories about {topic}",
    verbose=True,
    memory=True,
    backstory=(
        "With a flair for simplifying complex topics, you craft"
        "engaging narratives that captivate and educate, bringing new"
        "discoveries to light in an accessible manner."
    ),
    tools=[tool],
    llm=llm,
    allow_delegation=False,
)

writer_rag = Agent(
    role="Query Answerer using Web Search",
    goal="Create comprehensive and well-structured answers to given queries based on web search content.",
    backstory=(
        "Specialized in synthesizing information from multiple sources into "
        "coherent and engaging content while maintaining accuracy."
    ),
    tools=[tool],  # Ensure 'tool' is suitable for web search tasks
    llm=llm,  # Ensure 'llm' is configured for this agent's needs
    verbose=True,
    memory=True,
    allow_delegation=False,
)

rag_agent = Agent(
    role="RAG agent that answer of given query in quick manner along with citation using provided context only don't search on only of you don't found relvatent context then denie to give answer and also answer give in given format",
    goal="Create comprehensive and well-structured answers to given queries with citation based on given context only and also give the answer in given format.",
    backstory=(
        "Specialized in synthesizing information from multiple sources into "
        "coherent and engaging content while maintaining accuracy."
    ),  # Ensure 'tool' is suitable for web search tasks
    llm=llm,  # Ensure 'llm' is configured for this agent's needs
    verbose=True,
    memory=True,
    allow_delegation=False,
)
