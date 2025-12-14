import os
import chainlit as cl
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# Konfiguracja Gita wewnątrz kontenera (można to zrobić ładniej przez SSH)
# W produkcji użyjemy tokena z ENV
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

@cl.on_chat_start
def start():
    # Definicja Agentów
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

    # 1. Senior Developer
    coder = Agent(
        role='Senior Full Stack Developer',
        goal='Create fully functional apps with Docker Compose support',
        backstory='You are an expert coder. You always prefer Docker Compose over plain Dockerfiles.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    # 2. DevOps Engineer (Kluczowy dla Twojego workflow)
    devops = Agent(
        role='DevOps Engineer',
        goal='Create configuration files for deployment',
        backstory="""You are responsible for creating the docker-compose.yml file. 
        CRITICAL RULE: The docker-compose.yml MUST use variable ${IMAGE_NAME} for image 
        and ${HOST_PORT}:InternalPort for ports to accept the CI/CD pipeline inputs.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    cl.user_session.set("coder", coder)
    cl.user_session.set("devops", devops)

@cl.on_message
async def main(message: cl.Message):
    coder = cl.user_session.get("coder")
    devops = cl.user_session.get("devops")

    # Zadanie 1: Napisz kod aplikacji
    task_code = Task(
        description=f"Create a simple web app based on this request: {message.content}. Provide code for logic and UI.",
        agent=coder,
        expected_output="Source code files (e.g. index.js, package.json or main.py, requirements.txt)"
    )

    # Zadanie 2: Przygotuj konteneryzację
    task_docker = Task(
        description="""Create a Dockerfile and docker-compose.yml for the app created in previous step.
        The docker-compose.yml MUST follow this specific template structure:
        
        version: '3.8'
        services:
          app:
            image: ${IMAGE_NAME}
            ports:
              - "${HOST_PORT}:3000" (adjust internal port if needed)
        """,
        agent=devops,
        expected_output="Dockerfile and docker-compose.yml content"
    )

    crew = Crew(
        agents=[coder, devops],
        tasks=[task_code, task_docker],
        verbose=True
    )

    # Uruchomienie (synchroniczne w tym przykładzie)
    result = crew.kickoff()

    # Tutaj normalnie nastąpiłby zapis plików na dysk i GIT PUSH
    # Na potrzeby demo wyświetlamy wynik
    await cl.Message(content=f"Agenci zakończyli pracę:\n\n{result}").send()