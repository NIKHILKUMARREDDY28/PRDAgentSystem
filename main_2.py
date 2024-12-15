import streamlit as st
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv, find_dotenv
import yaml

# Load environment variables
load_dotenv(find_dotenv())

# Load agent configurations
def load_agent_configs(file_path: str):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        st.error(f"Failed to load agent configurations: {e}")
        return {}

agents_config = load_agent_configs('agents.yaml')

# Initialize agents
def initialize_agents(config):
    try:
        return {
            "UI/UX Agent 🖌️": Agent(**config['ui_ux_agent']),
            "Product Agent 📈": Agent(**config['product_agent']),
            "Engineering Agent 💻": Agent(**config['engineering_agent']),
            "Summarization Agent 📝": Agent(**config['summarization_agent'])
        }
    except KeyError as e:
        st.error(f"Missing agent configuration: {e}")
        return {}

agents = initialize_agents(agents_config)

# Define tasks
def define_tasks(agents):
    return {
        "UI/UX Agent 🖌️": Task(
            description="Provide UI/UX feedback on the product requirements.",
            expected_output="Feedback on user interface and experience aspects.",
            agent=agents.get("UI/UX Agent 🖌️")
        ),
        "Product Agent 📈": Task(
            description="Provide product management feedback on the product requirements.",
            expected_output="Feedback on product management aspects.",
            agent=agents.get("Product Agent 📈"),
        ),
        "Engineering Agent 💻": Task(
            description="Provide engineering feedback on the product requirements.",
            expected_output="Feedback on technical feasibility and implementation.",
            agent=agents.get("Engineering Agent 💻")
        ),
        "Summarization Agent 📝": Task(
            description="Consolidate feedback from all agents and provide a clear and actionable summary to finalize the development plan.",
            expected_output="A comprehensive summary that integrates all feedback and outlines the next steps for development.",
            agent=agents.get("Summarization Agent 📝")
        )
    }

tasks = define_tasks(agents)

# Initialize Crew with sequential task execution
crew = Crew(
    agents=list(agents.values()),
    tasks=list(tasks.values()),
    process=Process.sequential  # Ensures tasks are executed in order
)

# Custom CSS for improved UI
def apply_custom_css():
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
        </style>
        """,
        unsafe_allow_html=True,
    )

apply_custom_css()

# Sidebar for input and agent selection
def display_sidebar():
    st.sidebar.title("📝 Input Panel")
    st.sidebar.write("Provide the product requirements and select agents for feedback.")
    product_requirements = st.sidebar.text_area(
        "Enter Product Requirements:",
        placeholder="e.g., Develop a mobile app that allows users to track their daily fitness activities.",
        help="Describe the features and functionalities you want in the product."
    )
    selected_agents = st.sidebar.multiselect(
        "Select Agents for Discussion:",
        options=list(agents.keys()),
        default=list(agents.keys()),  # Include all agents by default
        help="Choose which agents you want feedback from."
    )
    generate_button = st.sidebar.button("🚀 Generate Discussion")
    return product_requirements, selected_agents, generate_button

product_requirements_input, selected_agent_names, generate_button = display_sidebar()

# Main content area
st.markdown('<div class="header-text">Product Requirements Discussion Simulator</div>', unsafe_allow_html=True)

# Agent descriptions
st.header("🤖 Agent Descriptions")
st.markdown("""
- **UI/UX Agent 🖌️:** Focuses on user interface and experience.
- **Product Agent 📈:** Handles product management perspectives.
- **Engineering Agent 💻:** Addresses technical feasibility and implementation.
- **Summarization Agent 📝:** Consolidates feedback and provides an actionable summary.
""")

# Generate discussion logic
if generate_button:
    if not product_requirements_input.strip():
        st.error("❗ Product requirements cannot be empty. Please provide details to proceed.")
    elif not selected_agent_names:
        st.error("❗ Please select at least one agent for the discussion.")
    else:
        # Filter agents and tasks
        selected_tasks = [tasks[agent] for agent in selected_agent_names if agent in tasks]
        selected_agents = [agents[agent] for agent in selected_agent_names if agent in agents]

        # Update crew
        crew.agents = selected_agents
        crew.tasks = selected_tasks

        # Generate discussion
        with st.spinner("🛠️ Generating discussion..."):
            try:
                results = crew.kickoff(inputs={'prd_content': product_requirements_input})
                st.success("🎉 Discussion generated successfully!")

                # Display discussion results
                st.header("💬 Discussion")
                with st.expander("📄 Product Requirements", expanded=True):
                    st.write(product_requirements_input)

                if hasattr(results, 'tasks_output'):
                    for task_output in results.tasks_output:
                        if task_output.agent == "Summarization Agent 📝":
                            st.header("📋 Consolidated Summary")
                            st.write(task_output.raw)
                        else:
                            st.subheader(f"{task_output.agent} Feedback")
                            st.write(task_output.raw)

                    # Download discussion as text file
                    st.download_button(
                        label="📥 Download Discussion",
                        data="\n\n".join([f"{task_output.agent}: {task_output.raw}" for task_output in results.tasks_output]),
                        file_name="discussion.txt",
                        mime="text/plain"
                    )
                else:
                    st.warning("No feedback generated. Please check inputs and agents.")
            except Exception as e:
                st.error(f"Error during discussion generation: {e}")
