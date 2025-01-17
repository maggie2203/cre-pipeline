import openai
import requests

# Set your OpenAI API key
openai.api_key = "your_openai_api_key"

import openai

# Set your OpenAI API key
openai.api_key = "your_openai_api_key"

def chat_with_gpt(prompt):
    """
    Sends a prompt to GPT using the updated OpenAI library and returns the response.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Specify the GPT model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error interacting with GPT: {e}"

def process_file_with_flask_api(file_path, api_url="http://localhost:5000/process"):
    """
    Sends a file to the Flask API for processing and retrieves the result.
    """
    try:
        with open(file_path, 'rb') as file:
            response = requests.post(api_url, files={"files": file})
        
        if response.status_code == 200:
            return response.json()  # Return the API response
        else:
            return {"status": "error", "message": response.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def gpt_bot_logic(user_input, file_path=None):
    """
    Main logic for the GPT bot.
    - If a file is provided, it processes the file via the Flask API.
    - If no file is provided, it interacts with GPT.
    """
    if file_path:
        api_response = process_file_with_flask_api(file_path)
        if api_response.get("status") == "success":
            return f"File processed successfully! Results are in {api_response.get('output_file')}."
        else:
            return f"Error processing file: {api_response.get('message')}."
    else:
        return chat_with_gpt(user_input)

# Example usage
if __name__ == "__main__":
    print("Welcome to the GPT Bot!")
    while True:
        user_input = input("Enter your message (or type 'file' to upload): ").strip()
        if user_input.lower() == "file":
            file_path = input("Enter the file path: ").strip()
            response = gpt_bot_logic("", file_path=file_path)
        else:
            response = gpt_bot_logic(user_input)
        
        print(response)
