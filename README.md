# 📊 Business Metrics Analysis Agent (LangGraph + LLM)

This project is a smart business analysis agent built using [LangGraph](https://python.langchain.com/docs/langgraph/) and large language models (LLMs) like OpenAI or Gemini (Google Generative AI). It evaluates daily business metrics such as sales, cost, profit, and customer acquisition cost (CAC), and provides insights including alerts and actionable recommendations.


## 🚀 Features

- Calculates profit, percentage changes in sales and cost, and CAC increases
- Detects significant CAC changes
- Uses LLM to generate business alerts and recommendations
- Graph-based modular processing using LangGraph
- **Validates input state using Pydantic for robust and clean type enforcement**
- Includes a test suite for validating business logic


## 📁 Project Structure

```
.

├── bussinessAgent.ipynb # (Optional) Jupyter notebook for interactive exploration
├── environment.yml # Conda environment configuration file
├── graph_export.py # Script to export LangGraph for LangGraph Studio
├── langgraph.json # Configuration for LangGraph Studio
├── main.py # Optional entry point to run the agent standalone
├── README.md # Main project documentation
└── src # Source code directory
    ├── agent.py # LangGraph agent and node logic
    ├── models.py # Pydantic models for structured input/output
    └── init.py
└── tests # Test suite using pytest
    ├── conftest.py # Shared fixtures for tests (e.g., LLM instances)
    ├── test_agent.py # Unit tests for agent nodes and logic
    └── __init__.py
    
```


## ✅ Environment Setup

### 1. Clone the Repository

```bash
git clone git@github.com:armachino/simple-business-agent.git
cd simple-business-agent
```

### 2. Install Dependencies (via Conda)

```bash
conda env create -f environment.yml
conda activate business-agent
```


## 🔐 API Keys Required

To run this project, you **must set the following environment variables** in your system or `.env` file:

| Variable                 | Description                                |
|--------------------------|--------------------------------------------|
| `OPENAI_API_KEY`         | (If using OpenAI models)                   |
| `GOOGLE_API_KEY`         | (If using Gemini/GGEA via LangChain)       |
| `LANGSMITH_API_KEY`      | (Optional, for LangSmith logging)          |
| `SMITH_LANGCHAIN_API_KEY`| (Optional, for LangSmith + LangChain tools)|

Example `.env`:

```
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
LANGSMITH_API_KEY=your_langsmith_key
SMITH_LANGCHAIN_API_KEY=your_smith_key
```

💡 Use `python-dotenv` to load `.env` if needed:
> ```python
> from dotenv import load_dotenv
> load_dotenv()
> ```


## Running the Agent

You can run the program directly using the `main.py` entry point:

```bash
python main.py
```


## 📺 LangGraph Studio

**LangGraph Studio** is a visual interface that lets you run, debug, and inspect your LangGraph step-by-step. It helps you understand how data flows through your agent and makes development easier.

To use it, simply run the following command inside your project workspace:

```bash
langgraph dev
```

This will launch the Studio locally, allowing you to interactively test and explore your agent.


## 🧪 Testing

This project uses **pytest** for testing. To run tests:

```bash
pytest
```

This will:
- Validate metric calculations (profit, % change, CAC)
- Ensure business logic and alerts function as expected


## 📌 Notes

- `Agent` class defines a LangGraph with two nodes: `processing_node`, and `recommendation_node`
- Prompting is handled through `ChatPromptTemplate`
- Output is parsed using `RegexParser`
- Designed to be extensible and modular
- Uses Pydantic models to ensure clean validation and type safety
- Compatible with LangGraph Studio by exposing the `graph` property
