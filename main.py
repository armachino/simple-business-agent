import sys
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from src.models import InputState
from src.agent import Agent 

def main():

    # Initialize the model
    # You can use either "ChatGoogleGenerativeAI" or "ChatOpenAI" based on your preference.

    #   ChatGoogleGenerativeAI
    model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0,
    )
    #  ChatOpenAI
    # model = ChatOpenAI(model="gpt-4o", temperature=0)

    # Example input state dict
    # This should match the structure defined in your InputState model.
    input_state_dict = {
        "today": {"sales": 1000.0, "cost": 1200.0, "number_of_customers": 30},
        "previous_day": {"sales": 900.0, "cost": 1000.0, "number_of_customers": 40},
    }

    input_state = InputState.model_validate(input_state_dict)
    agent = Agent(model)
    print(agent.graph.invoke(input_state.model_dump()))  # type: ignore

if __name__ == "__main__":
    main()