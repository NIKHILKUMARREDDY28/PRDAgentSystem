import streamlit as st
from crewai import Agent, Task, Crew
from dotenv import load_dotenv, find_dotenv

from utils import MyCustomHandler

# Load environment variables
load_dotenv(find_dotenv())
# Load agent configurations
import yaml

with open('agents.yaml', 'r') as file:
    agents_config = yaml.safe_load(file)

# Initialize agents
ui_ux_agent = Agent(**agents_config['ui_ux_agent'])
product_agent = Agent(**agents_config['product_agent'])
engineering_agent = Agent(**agents_config['engineering_agent'])


ui_ux_task = Task(

    description="Provide UI/UX feedback on the product requirements.",
    expected_output="The UI/UX agent should provide feedback on the user interface and user experience aspects of the product requirements.",
    agent=ui_ux_agent
)

product_task = Task(
    description="Provide product management feedback on the product requirements.",
    expected_output="The product agent should provide feedback on the product management aspects of the product requirements.",
    agent=product_agent,

)

engineering_task = Task(
    description="Provide engineering feedback on the product requirements.",
    expected_output="The engineering agent should provide feedback on the technical feasibility and implementation aspects of the product requirements.",
    agent=engineering_agent
)

# Create the crew
crew = Crew(
    agents=[ui_ux_agent, product_agent, engineering_agent],
    tasks=[ui_ux_task, product_task, engineering_task]
)

# Streamlit UI
st.title("Product Requirements Discussion Simulator")

prd_input = st.text_area("Enter Product Requirements:")

if st.button("Generate Discussion"):
    if prd_input:
        inputs = {'prd_content': prd_input}
        results = crew.kickoff(inputs=inputs)
        for task_output in results.tasks_output:
            st.subheader(f"{task_output.agent}:")
            st.markdown(task_output.raw)
    else:
        st.error("Please enter the product requirements.")

