from backend import config
from backend.db_functions import *
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
    responses = []
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

        response = prompt_ai(ai["id"], "system", startingPrompt, True)
        responses.append(response)

    print("-----Responses-----")
    print(responses)
    return responses


def prompt_ai(ai_id: int, prompt_role: str, prompt: str, isAction: bool):
    # Generate message history
    messages = []
    systemMessage = select_system_message(ai_id)
    messageHistory = generate_message_history(ai_id)

    messages.append({"role": "system", "content": systemMessage[0]})
    for message in messageHistory:
        messages.append({"role": message[0], "content": message[1][0]})
        messages.append({"role": "assistant", "content": message[2][0]})

    # Add the prompt to the messages
    messages.append({"role": prompt_role, "content": prompt})

    print("-----Messages-----")
    print(messages)

    # Quiry the AI
    if isAction:
        completion = client.chat.completions.create(
            model=config.model,
            max_tokens=config.max_tokens,
            response_format={"type": "json_object"},
            messages=messages,
        )
        responseStr = completion.choices[0].message.content
        jsonResponse = json.loads(responseStr)
        response = {"id": ai_id, "action": jsonResponse["action"]}
        insert_message(ai_id, prompt_role, prompt, f"I choose to {jsonResponse["action"]}")
    else:
        completion = client.chat.completions.create(
            model=config.model,
            max_tokens=config.max_tokens,
            messages=messages,
        )
        response = completion.choices[0].message.content
        insert_message(ai_id, prompt_role, prompt, response)

    # Return the response
    return response


def generate_message_history(ai_id):
    # Make a request to the db for the system message and messages related with the ai
    messageHistory = select_messages(ai_id)
    # If the message history is too long, shorten it.
    # Return the message history
    return messageHistory


# test_ais = [
#     {
#         "id": 0,
#         "name": "Joe",
#         "appearance": "A short, blonde man in his twenties",
#         "personality": "Extroverted and talkative",
#     },
#     {
#         "id": 1,
#         "name": "Jane",
#         "appearance": "A tall, brunette woman in her twenties",
#         "personality": "Introverted and shy",
#     },
# ]

# test_actions = ["Talk to someone", "Find a place to sit", "Find somewhere quiet"]

# start_simulation(test_ais, str(test_actions))
