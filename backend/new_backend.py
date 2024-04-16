import config
from db_functions import *
from openai import OpenAI
import json

client = OpenAI()


def start_simulation(ais, actions):
    # Create database
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

        prompt_ai(ai["id"], startingPrompt)


def prompt_ai(ai_id, prompt):
    systemMessage = select_system_message(ai_id)
    print(systemMessage)
    # Generate message history
    # Add the prompt to the messages
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
