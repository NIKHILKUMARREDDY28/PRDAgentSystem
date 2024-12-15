# PRD Agent System

The **PRD Agent System** is a collaborative AI-powered tool designed to streamline the product requirements discussion process. It leverages the CrewAI framework to orchestrate multiple specialized agents—UI/UX, Product, Engineering, and Summarization—to provide comprehensive feedback and actionable insights for product development.

## Features

- **UI/UX Agent 🖌️**: Provides feedback on user interface and experience.
- **Product Agent 📈**: Focuses on product management and strategic aspects.
- **Engineering Agent 💻**: Evaluates technical feasibility and implementation.
- **Summarization Agent 📝**: Consolidates feedback and offers a clear, actionable summary.
- **Streamlit Interface**: Interactive and user-friendly UI for seamless operation.
- **Dynamic Orchestration**: Customize agent selection for specific discussions.

---

## Setup Instructions

### Prerequisites

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/NIKHILKUMARREDDY28/PRDAgentSystem
   cd PRDAgentSystem
   ```

2.**Virtual Environment**: Create a virtual environment using anaconda.
3. **Dependencies**: Install required Python libraries using `pip`.
    ```bash
    pip install poetry
    ```


4.Install dependencies through poetry:
   ```bash
   poetry install
   ```

5.Set up environment variables:
   - Create a `.env` file in the project root.
   - Add the following variables:
     ```env
     OPENAPI_KEY=<Your OPENAI API Key>
     ```

6.Define agent configurations:
   - Update the `agents.yaml` file with your agents' roles, goals, and other configurations.

### Running the Application

1. Start the Streamlit server:
   ```bash
   streamlit run main_2.py
   ```

2. Open the application in your browser at `http://localhost:8501`.

---

## Usage

1. **Provide Product Requirements**:
   - Enter detailed product requirements in the input text area.

2. **Select Agents**:
   - Choose the agents you want to involve in the discussion from the sidebar.

3. **Generate Feedback**:
   - Click "🚀 Generate Discussion" to initiate the process.

4. **View and Export Results**:
   - Review agent-specific feedback and the consolidated summary.
   - Download the discussion results as a `.txt` file.

---

## Directory Structure

```
PRDAgentSystem/
├── main_2.py               # Main application file
├── agents.yaml             # Agent configurations
├── README.md               # Project documentation
├── .env                    # Environment variables (not included in the repository)
└── .gitignore              # Ignore sensitive files
```


