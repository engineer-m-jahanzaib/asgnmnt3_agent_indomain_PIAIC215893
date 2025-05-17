import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Your Gemini API Key from the .env file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def my_success_coach(prompt):
    # Gemini API endpoint using the API key
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }

    # Sample data to send to the API (customize this if needed)
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    # Send the request to the Gemini API
    response = requests.post(url, headers=headers, json=data)

    # Debugging: Print the response status and content
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.text)

    if response.status_code == 200:
        try:
            # Parse the response JSON
            result = response.json()
            print("API Response:", result)  # Debugging the response structure
            
            # Extract the relevant content from the response
            reply = result['candidates'][0]['content']['parts'][0]['text']
            print("Gemini says:", reply)
            return reply
        except Exception as e:
            print("Error while processing the response:", e)
            return "An error occurred while processing the response."
    else:
        print("Error in API request:", response.status_code)
        print(response.text)
        return "Error occurred. Please try again later."

def save_output_to_file(conversation):
    # Save the conversation to output.md at the root of the project with UTF-8 encoding
    output_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.md")
    with open(output_file_path, "w", encoding="utf-8") as file:
        for item in conversation:
            file.write(f"{item}\n\n")
    print("\n📝 The conversation has been saved to output.md!")

def run_success_coach():
    conversation_history = []
    print("🚀 Success Coach is ready to help you stay motivated!\n")

    while True:
        # Capture user's input
        user_input = input("💬 Your prompt: ").strip()

        if user_input.lower() == "exit":
            print("👋 Thanks for using Success Coach. Keep growing! 💪")
            break

        # Add timestamp to the conversation history
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conversation_history.append(f"🕒 Prompt Time: {current_time}\nPrompt: {user_input}\n")

        # Get the response from Success Coach
        response = my_success_coach(user_input)

        # Add response time to the conversation history
        response_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conversation_history.append(f"🕒 Response Time: {response_time}\n{response}\n")

        print(f"\n🧠 Success Coach:\n{response}\n")

    # After the session ends, save the conversation to output.md
    save_output_to_file(conversation_history)

# Call the function to run the agent
if __name__ == "__main__":
    run_success_coach()
