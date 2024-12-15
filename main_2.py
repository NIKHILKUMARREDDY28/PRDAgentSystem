import streamlit as st
from crewai import Agent, Task, Crew
from dotenv import load_dotenv, find_dotenv
import yaml

# Load environment variables
load_dotenv(find_dotenv())
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# Load agent configurations
with open('agents.yaml', 'r') as file:
    agents_config = yaml.safe_load(file)

# Initialize agents
ui_ux_agent = Agent(**agents_config['ui_ux_agent'])
product_agent = Agent(**agents_config['product_agent'])
engineering_agent = Agent(**agents_config['engineering_agent'])

# Define tasks
ui_ux_task = Task(
    description="Provide UI/UX feedback on the product requirements.",
    expected_output="Feedback on user interface and experience aspects.",
    agent=ui_ux_agent
)

product_task = Task(
    description="Provide product management feedback on the product requirements.",
    expected_output="Feedback on product management aspects.",
    agent=product_agent,
)

engineering_task = Task(
    description="Provide engineering feedback on the product requirements.",
    expected_output="Feedback on technical feasibility and implementation.",
    agent=engineering_agent
)

# Create the crew
crew = Crew(
    agents=[ui_ux_agent, product_agent, engineering_agent],
    tasks=[ui_ux_task, product_task, engineering_task]
)

# Custom CSS for enhanced UI
st.markdown(
    """
    <style>
    .main {
        padding: 20px;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        font-size: 16px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .stTextInput, .stMultiselect {
        margin-bottom: 15px;
    }
    .st-expander {
        margin-bottom: 20px;
    }
    .header-text {
        text-align: center;
        margin-top: 30px;
        font-size: 28px;
        font-weight: bold;
    }
    .footer {
        text-align: center;
        margin-top: 50px;
        font-size: 14px;
        color: grey;
    }
    .sidebar .stTextInput, .sidebar .stMultiselect {
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)



# Sidebar for input and agent selection
with st.sidebar:
    st.title("📝 Input Panel")
    st.write("Provide the product requirements and select agents for feedback.")

    # Text area for product requirements input with placeholder and help text
    product_requirements_input = st.text_area(
        "Enter Product Requirements:",
        placeholder="e.g., Develop a mobile app that allows users to track their daily fitness activities.",
        help="Describe the features and functionalities you want in the product."
    )

    # Agent selection
    agent_options = {
        "UI/UX Agent 🖌️": ui_ux_agent,
        "Product Agent 📈": product_agent,
        "Engineering Agent 💻": engineering_agent
    }
    selected_agent_names = st.multiselect(
        "Select Agents for Discussion:",
        options=list(agent_options.keys()),
        default=list(agent_options.keys()),
        help="Choose which agents you want feedback from."
    )

    # Button to generate discussion
    generate_button = st.button("🚀 Generate Discussion")

# Main content area
st.markdown('<div class="header-text">Product Requirements Discussion Simulator</div>', unsafe_allow_html=True)

# Display agent descriptions
st.header("🤖 Agent Descriptions")
st.markdown("""
- **UI/UX Agent 🖌️:** Focuses on user interface and experience.
- **Product Agent 📈:** Handles product management perspectives.
- **Engineering Agent 💻:** Addresses technical feasibility and implementation.
""")

# Handle the "Generate Discussion" button click
if generate_button:
    if product_requirements_input.strip():
        if selected_agent_names:
            # Filter agents and tasks based on selection
            selected_agents = [agent_options[name] for name in selected_agent_names]
            selected_tasks = []
            if "UI/UX Agent 🖌️" in selected_agent_names:
                selected_tasks.append(ui_ux_task)
            if "Product Agent 📈" in selected_agent_names:
                selected_tasks.append(product_task)
            if "Engineering Agent 💻" in selected_agent_names:
                selected_tasks.append(engineering_task)

            # Update crew with selected agents and tasks
            crew.agents = selected_agents
            crew.tasks = selected_tasks

            inputs = {'prd_content': product_requirements_input}

            # Show a spinner and progress bar while generating discussion
            with st.spinner("🛠️ Generating discussion..."):
                results = crew.kickoff(inputs=inputs)

            st.success("🎉 Discussion generated successfully!")

            # Display the discussion
            st.header("💬 Discussion")

            # Display the product requirements as a message from the user
            with st.expander("📄 Product Requirements", expanded=True):
                st.write(product_requirements_input)

            # Create tabs for each agent's feedback
            if results and hasattr(results, 'tasks_output'):
                agent_names = [task_output.agent for task_output in results.tasks_output]
                agent_outputs = [task_output.raw for task_output in results.tasks_output]

                tabs = st.tabs(agent_names)

                for tab, agent_name, agent_output in zip(tabs, agent_names, agent_outputs):
                    with tab:
                        st.markdown(f"**{agent_name} says:**")
                        st.write(agent_output)

                # Option to download the discussion
                st.header("📥 Export Discussion")
                discussion_text = f"**Product Requirements:**\n{product_requirements_input}\n\n"
                for agent_name, agent_output in zip(agent_names, agent_outputs):
                    discussion_text += f"**{agent_name} Feedback:**\n{agent_output}\n\n"

                st.download_button(
                    label="Download Discussion as Text File",
                    data=discussion_text,
                    file_name="discussion.txt",
                    mime="text/plain"
                )

                # Provide a summary or key takeaways
                st.header("📝 Summary")
                for agent_name, agent_output in zip(agent_names, agent_outputs):
                    # Simple summary: first sentence of the agent's feedback
                    summary = agent_output.split('.')[0] + '.' if '.' in agent_output else agent_output
                    st.write(f"**{agent_name}:** {summary}")
            else:
                st.warning("No feedback was generated. Please check your inputs and try again.")
        else:
            st.error("❗ Please select at least one agent for the discussion.")
    else:
        st.error("❗ Product requirements cannot be empty. Please provide details to proceed.")
