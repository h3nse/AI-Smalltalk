import config
from db_functions import *
from openai import OpenAI
import json
from time import sleep

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
        insert_ai(ai["id"], ai["name"], ai["appearance"], ai["personality"])

        startingPrompt = f"""You enter a small party. 
Pick one of the following actions, formatted as valid JSON in the form \"action\": \"your chosen action\"

Available actions:
{actions}"""

        response = prompt_ai(ai["id"], "system", startingPrompt, True)
        responses.append(response)

    print(responses)

    return responses


def prompt_ai(ai_id: int, prompt_role: str, prompt: str, isAction: bool):
    # Generate message history
    messages = []
    systemMessageContent = select_system_message_content(ai_id)
    systemMessage = f"""You are roleplaying as a character at a party named {systemMessageContent[0]} with these traits:
Appearance:
{systemMessageContent[1]}
Personality:
{systemMessageContent[2]}"""

    messageHistory = generate_message_history(ai_id)

    print(f"-----AI{ai_id} MESSAGE HISTORY-----")
    messages.append({"role": "system", "content": systemMessage})
    print(f"system: {systemMessage}\n")
    for message in messageHistory:
        messages.append({"role": message[0], "content": message[1]})
        print(f"{message[0]}: {message[1]}\n")

    # Add the prompt to the messages
    messages.append({"role": prompt_role, "content": prompt})
    print(f"{prompt_role}: {prompt}\n")

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
        action = jsonResponse["action"]
        insert_message(ai_id, "system", f"You choose to {action}")
        response = {"id": ai_id, "action": action}
    else:
        completion = client.chat.completions.create(
            model=config.model,
            max_tokens=config.max_tokens,
            messages=messages,
        )
        response = completion.choices[0].message.content
        insert_message(ai_id, prompt_role, prompt)
        insert_message(ai_id, "assistant", response)

    # Return the response
    print(f"assistant: {response}")
    return response


def generate_message_history(ai_id):
    # Make a request to the db for the system message and messages related with the ai
    messageHistory = select_messages(ai_id)

    # TODO: If the message history is too long, shorten it.

    # Return the message history
    return messageHistory


def start_conversation(approacherId: int, recipientId: int):
    # Prompt approacher with the appearance of the recipient
    systemMessageContent = select_system_message_content(recipientId)
    recipientAppearance = systemMessageContent[1]
    prompt = f"You approach another party-goer with these physical traits: {recipientAppearance}. What do you say?"
    response = prompt_ai(approacherId, "system", prompt, False)

    # Prompt the approachers opening message, along with their appearance, to the recipient
    systemMessageContent = select_system_message_content(approacherId)
    approacherAppearance = systemMessageContent[1]
    prompt = f'You get aproached by another party-goer with these physical traits: {approacherAppearance}. They start the conversation by saying: "{response}". Your reply: '
    response = prompt_ai(recipientId, "system", prompt, False)

    # Loop promptings back and forth, until the conversation is ended or the max amount of messages is reached
    while True:
        sleep(3)
        response = prompt_ai(approacherId, "user", response, False)
        sleep(3)
        response = prompt_ai(recipientId, "user", response, False)


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

test_actions = ["Talk to someone", "Find a place to sit", "Find somewhere quiet"]

start_simulation(test_ais, str(test_actions))
start_conversation(0, 1)
