# pseudo-kod logiki agentowej (main.py)
from crewai import Agent, Task, Crew
from langchain_community.tools import ReadFileTool, WriteFileTool
from tools.git_tools import GitPushTool # Własne narzędzie do Gita

# 1. Definicja Agentów
dev_agent = Agent(
    role='Senior Python Developer',
    goal='Write clean, containerized code',
    backstory='Expert in Python and Docker.',
    allow_delegation=False
)

qa_agent = Agent(
    role='Code Reviewer',
    goal='Ensure code quality and safety',
    backstory='Strict auditor who checks for security flaws and logic errors.',
    allow_delegation=False
)

git_agent = Agent(
    role='Git Operator',
    goal='Push code to repository',
    tools=[GitPushTool()],
    backstory='Responsible for version control operations.'
)

# 2. Definicja Zadań (Dynamicznie tworzona na podstawie Twojego promptu)
task_code = Task(description=user_prompt, agent=dev_agent)
task_review = Task(description="Review the code. If bad, ask Dev to fix.", agent=qa_agent)
task_push = Task(description="Push the approved code to branch 'feature/ai-app'", agent=git_agent)

# 3. Uruchomienie Załogi
crew = Crew(
    agents=[dev_agent, qa_agent, git_agent],
    tasks=[task_code, task_review, task_push],
    verbose=True
)

result = crew.kickoff()