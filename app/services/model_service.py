from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr


def get_gemini_model(
        google_api_key: str,
        model="gemini-1.5-pro",
        temperature=0,
):
    return ChatGoogleGenerativeAI(
        model=model,
        google_api_key=SecretStr(google_api_key),
        temperature=temperature
    )
