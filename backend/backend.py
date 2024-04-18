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

    messages.append({"role": "system", "content": systemMessage})
    for message in messageHistory:
        messages.append({"role": message[0], "content": message[1]})

    # Add the prompt to the messages
    messages.append({"role": prompt_role, "content": prompt})

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
    recipientSystemMessageContent = select_system_message_content(recipientId)
    recipientAppearance = recipientSystemMessageContent[1]
    prompt = f"You approach another party-goer with these physical traits: {recipientAppearance}. What do you say?"
    response1 = prompt_ai(approacherId, "system", prompt, False)

    # Prompt the approachers opening message, along with their appearance, to the recipient
    approacherSystemMessageContent = select_system_message_content(approacherId)
    approacherAppearance = approacherSystemMessageContent[1]
    prompt = f'You get aproached by another party-goer with these physical traits: {approacherAppearance}. They start the conversation by saying: "{response1}". Your reply: '
    response2 = prompt_ai(recipientId, "system", prompt, False)

    # Loop promptings back and forth, until the conversation is ended or the max amount of messages is reached
    for i in range(config.max_conversation_iterations):
        if i == config.max_conversation_iterations - 1:
            response2 += "(System note: Please end conversation soon)"
            print("(System note: Please end conversation soon)")

        # Give responses back and forth
        response1 = prompt_ai(approacherId, "user", response2, False)
        sleep(len(response1) * config.message_wait_time_multiplier)
        response2 = prompt_ai(recipientId, "user", response1, False)
        sleep(len(response1) * config.message_wait_time_multiplier)

        # Check if conversation is coming to a close
        systemMessage = f"""You are an AI part of a larger system, where a conversation is being simulated. 
        Your job is to detect when the conversation is ending naturally, so that the system can end the conversation. 
        You will be given the last parts of a conversation, and will have to determine wether to end the conversation. 
        Please reply in valid JSON in the format \"endConversation\": \"True/False\"
        conversation:
        {approacherSystemMessageContent[0]}: {response1} 
        {recipientSystemMessageContent[0]}: {response2}
        """

        messages = []
        messages.append({"role": "system", "content": systemMessage})
        completion = client.chat.completions.create(
            model=config.model,
            max_tokens=config.max_tokens,
            response_format={"type": "json_object"},
            messages=messages,
        )
        responseStr = completion.choices[0].message.content
        jsonResponse = json.loads(responseStr)
        print(jsonResponse)
        endConversation = jsonResponse["endConversation"] == "True"

        if endConversation:
            print("Ending conversation")
            break
    print("Conversation ended")


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
