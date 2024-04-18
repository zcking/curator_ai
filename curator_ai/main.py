import os
import json
from datetime import datetime

from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, YoutubeVideoSearchTool

# To use DBRX model, set the following environment variables
os.environ['OPENAI_API_KEY'] = 'NA'
os.environ['OPENAI_MODEL_NAME'] = 'databricks-dbrx-instruct'
# os.environ['OPENAI_API_BASE'] = 'https://yourworkspace.cloud.databricks.com/serving-endpoints'
# os.environ['SERPER_API_KEY'] = 'changeme'

# Override default LLM with Databricks DBRX model
from langchain_community.chat_models import ChatDatabricks

llm = ChatDatabricks(
    endpoint=os.environ['OPENAI_MODEL_NAME'],
)

search_tool = SerperDevTool()
youtube_tool = YoutubeVideoSearchTool()

today = datetime.today().strftime('%Y-%m-%d %H-%M')

researcher = Agent(
    role='Senior Research Analyst',
    goal='Uncover cutting-edge developments in AI, data, software engineering',
    backstory="""You work at a leading tech think tank.
    Your expertise lies in identifying emerging credible tech trends from blogs, articles, and videos.
    You have a knack for dissecting complex data and presenting actionable insights.""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, youtube_tool],
    llm=llm,
)

writer = Agent(
    role='Tech Content Strategist',
    goal='Create engaging content on tech advancements in AI, data, and software engineering',
    backstory="""You are a renowned Content Strategist, known for your insightful
    and engaging tech articles. You have a keen eye for captivating narratives and real-world applications.""",
    verbose=True,
    allow_delegation=True,
    llm=llm,
)

# Create tasks for your agents
task1 = Task(
    description="""Conduct a comprehensive analysis of the latest advancements in tech,
    focusing on fields like AI, data engineering, software engineering, AWS and Azure cloud, and Databricks 
    in the past month from 2024. Identify key trends, breakthrough technologies, and potential impact on industries.""",
    expected_output="Full analysis report in bullet points",
    agent=researcher,
)

task2 = Task(
    description="""Using the insights provided, provide 10 or more suggestions for engaging blog posts, videos, and projects,
    that highlight the most significant advancements in fields like AI, data engineering, software engineering, AWS and Azure cloud, and Databricks.
    Your suggestions should focus on real-world use cases and cater to a tech-savvy audience.
    The projects should be specific ideas and small enough to be completed within 1-4 weeks.
    Make it sound cool, avoid complex words so it doesn't sound like AI generated.""",
    expected_output="Numbered list of engaging blog post ideas, project suggestions, and video ideas",
    agent=writer,
)


def main():
    # Assemble your crew with a sequential process
    crew = Crew(
        agents=[researcher, writer],
        tasks=[task1, task2],
        verbose=2, # Set the verbosity level to 1 or 2 for different logging levels
        output_log_file=f"logs/crew_{today}.log",
    )

    # Start the crew to work
    result = crew.kickoff()

    print('#' * 30)
    print(result)

    # Append crew.usage_metrics to the log file
    with open(f"logs/crew_{today}.log", "a") as text_file:
        text_file.write('\n\n')
        text_file.write(json.dumps(crew.usage_metrics, indent=2))

    # Save the result to a file with today's date
    with open(f"outputs/result_{today}.md", "w") as text_file:
        text_file.write(result)


if __name__ == '__main__':
    main()
