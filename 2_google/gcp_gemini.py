import google.generativeai as genai
import os


def generate_content(model: genai.GenerativeModel, inquiry: str) -> str:
    """Generate content using the model

    Args:
        model (genai.GenerativeModel): The model to generate content from
        inquiry (str): The prompt to generate content from

    Returns:
        None
    """
    response = model.generate_content(inquiry)
    print(response.text)
    return response.text

def start_chat(model: genai.GenerativeModel, inquiry: str = None) -> str:
    """Start a chat with the model

    Args:
        model (genai.GenerativeModel): The model to chat with
        inquiry (str): The prompt to start the chat with

    Returns:
        None
    """
    chat = model.start_chat()
    response = chat.send_message("What should I eat for breakfast?")
    yield response.text
    response = chat.send_message("What about lunch?")
    yield response.text


def main():
    genai.configure(api_key=os.environ['GOOGLE_CLOUD_API_KEY'])
    model = genai.GenerativeModel('gemini-pro')
    generate_content(model, 'What is the capital of France?')

    for resp in start_chat(model):
        print(resp)
    

if __name__ == "__main__":
    main()