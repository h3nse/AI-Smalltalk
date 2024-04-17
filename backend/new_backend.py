import config
from db_functions import *
from openai import OpenAI
import json

client = OpenAI()


def start_simulation(ais, actions):
    # Reset database
    reset_databases()
    create_databases()

    # For each ai:
    #   - Create a system message
    #   - Save the system message in the db
    #   - Create a starting prompt
    #   - Run prompt_ai
    for ai in ais:
        systemMessage = f"""You are roleplaying as a character named {ai['name']} with these traits:

                        Appearance:
                        {ai['appearance']}

                        Personality:
                        {ai['personality']}"""

        insert_ai(ai["id"], systemMessage)

        startingPrompt = f"""You enter a small party. 
                        Pick one of the following actions, formatted as valid JSON in the form \"action\": [your chosen action]
                        
                        Available actions:
                        {actions}"""

        prompt_ai(ai["id"], "system", startingPrompt)


def prompt_ai(ai_id: int, prompt_role: str, prompt: str):
    # Generate message history
    messages = []
    systemMessage = select_system_message(ai_id)
    chatHistory = select_messages(ai_id)

    messages.append({"role": "system", "content": systemMessage})
    for chat in chatHistory:
        messages.append({"role": chat[0], "content": chat[1]})
        messages.append({"role": "assistant", "content": chat[2]})

    # Add the prompt to the messages
    messages.append({"role": prompt_role, "content": prompt})

    print(messages)
    # Quiry the AI
    # Save the prompt and response to the db
    # Return the response


def generate_message_history(ai):
    # Make a request to the db for the system message and messages related with the ai
    # If the message history is too long, shorten it.
    # Return the message history
    pass


test_ais = [
    {
        "id": 0,
        "name": "Joe",
        "appearance": "A short, blonde man in his twenties",
        "personality": "Extroverted and talkative",
    },
    {
        "id": 1,
        "name": "Jane",
        "appearance": "A tall, brunette woman in her twenties",
        "personality": "Introverted and shy",
    },
]

test_actions = "Talk to someone, Find a place to sit, Find somewhere quiet"

start_simulation(test_ais, test_actions)
