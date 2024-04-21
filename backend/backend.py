from backend import config

# import config

from backend.db_functions import *

# from db_functions import *
from openai import OpenAI
import json
from time import sleep

client = OpenAI()

_updates = {"messages": [], "endedConversations": []}


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

    return responses


def prompt_ai(aiId: int, promptRole: str, prompt: str, isAction: bool):
    # Generate message history
    messages = []
    systemMessageContent = select_system_message_content(aiId)
    systemMessage = f"""You are roleplaying as a character at a party named {systemMessageContent[0]} with these traits:
Appearance:
{systemMessageContent[1]}
Personality:
{systemMessageContent[2]}"""

    messageHistory = generate_message_history(aiId)

    messages.append({"role": "system", "content": systemMessage})
    for message in messageHistory:
        messages.append({"role": message[0], "content": message[1]})

    # Add the prompt to the messages
    messages.append({"role": promptRole, "content": prompt})

    # Quiry the AI
    if isAction:
        completion = client.chat.completions.create(
            model=config.model,
            max_tokens=config.MAX_TOKENS,
            response_format={"type": "json_object"},
            messages=messages,
        )
        responseStr = completion.choices[0].message.content
        jsonResponse = json.loads(responseStr)
        action = jsonResponse["action"]
        insert_message(aiId, "system", f"You choose to {action}")
        response = {"id": aiId, "action": action}
    else:
        completion = client.chat.completions.create(
            model=config.model,
            max_tokens=config.MAX_TOKENS,
            messages=messages,
        )
        response = completion.choices[0].message.content
        insert_message(aiId, promptRole, prompt)
        insert_message(aiId, "assistant", response)

    # Return the response
    print(f"assistant: {response}")
    return response


def generate_message_history(aiId):
    # Make a request to the db for the system message and messages related with the ai
    messageHistory = select_messages(aiId)

    # TODO: If the message history is too long, shorten it.

    # Return the message history
    return messageHistory


def start_conversation(approacherId: int, recipientId: int):
    global _updates
    # Prompt approacher with the appearance of the recipient
    recipientSystemMessageContent = select_system_message_content(recipientId)
    recipientAppearance = recipientSystemMessageContent[1]
    prompt = f"You approach another party-goer with these physical traits: {recipientAppearance}. What do you say?"
    response1 = prompt_ai(approacherId, "system", prompt, False)
    _updates["messages"].append({"ai": approacherId, "content": response1})

    # Prompt the approachers opening message, along with their appearance, to the recipient
    approacherSystemMessageContent = select_system_message_content(approacherId)
    approacherAppearance = approacherSystemMessageContent[1]
    prompt = f'You get aproached by another party-goer with these physical traits: {approacherAppearance}. They start the conversation by saying: "{response1}". Your reply: '
    response2 = prompt_ai(recipientId, "system", prompt, False)
    _updates["messages"].append({"ai": recipientId, "content": response2})

    # Loop promptings back and forth, until the conversation is ended or the max amount of messages is reached
    for i in range(config.MAX_CONVERSATION_ITERATIONS):
        # Tell the AIs to stop the conversation if they're getting close to the limit
        if i == config.MAX_CONVERSATION_ITERATIONS - 1:
            response2 += "(System note: Please end conversation soon)"
            print("(System note: Please end conversation soon)")

        # Give responses back and forth
        response1 = prompt_ai(approacherId, "user", response2, False)
        _updates["messages"].append({"ai": approacherId, "content": response1})
        sleep(len(response1) * config.MESSAGE_WAIT_MULTIPLIER)

        response2 = prompt_ai(recipientId, "user", response1, False)
        _updates["messages"].append({"ai": recipientId, "content": response2})
        sleep(len(response1) * config.MESSAGE_WAIT_MULTIPLIER)

        # Check if conversation should be ended
        if check_conversation_end(response1, response2):
            _updates["endedConversations"].append([approacherId, recipientId])
            break
    print("Conversation ended")
    print(_updates)


def check_conversation_end(message1: str, message2: str) -> bool:
    systemMessage = f"""You are an AI part of a larger system, where a conversation is being simulated. 
        Your job is to detect when the conversation is ending naturally, so that the system can end the conversation. 
        You will be given the last parts of a conversation, and will have to determine wether to end the conversation. 
        Please reply in valid JSON in the format \"endConversation\": \"True/False\"
        conversation:
        person 1: {message1} 
        person 2: {message2}
        """

    messages = []
    messages.append({"role": "system", "content": systemMessage})
    completion = client.chat.completions.create(
        model=config.model,
        max_tokens=config.MAX_TOKENS,
        response_format={"type": "json_object"},
        messages=messages,
    )
    responseStr = completion.choices[0].message.content
    jsonResponse = json.loads(responseStr)
    return jsonResponse["endConversation"] == "True"


def read_updates():
    global _updates
    ### Returns the update variable and resets it
    returnUpdates = _updates.copy()
    _updates = {"messages": [], "endedConversations": []}
    return returnUpdates


# testAis = [
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

# testActions = ["Talk to someone", "Find a place to sit", "Find somewhere quiet"]

# start_simulation(testAis, str(testActions))
# start_conversation(0, 1)
