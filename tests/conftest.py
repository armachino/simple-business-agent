from langchain_google_genai import ChatGoogleGenerativeAI
import pytest

@pytest.fixture
def model():
    #   ChatGoogleGenerativeAI
    model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0,
    )
    #  ChatOpenAI
    # model = ChatOpenAI(model="gpt-4o", temperature=0)

    return model
