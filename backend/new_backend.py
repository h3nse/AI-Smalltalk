import config
from openai import OpenAI
import json

client = OpenAI()


def start_simulation():
    # For each ai:
    #   - Create a system message
    #   - Save the system message in the db
    #   - Create a starting prompt
    #   - Run prompt_ai
    pass


def prompt_ai(ai, prompt):
    # Generate message history
    # Add the prompt to the messages
    # Quiry the AI
    # Save the prompt and response to the db
    # Return the response
    pass


def generate_message_history(ai):
    # Make a request to the db for the system message and messages related with the ai
    # If the message history is too long, shorten it.
    # Return the message history
    pass
