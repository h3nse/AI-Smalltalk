import config
from openai import OpenAI
import json

client = OpenAI()

# The AI's chat history are stored here
messages_list = []


def start_simulation(actions, ais):

    # Add the customized system message for each ai
    for ai in ais:
        systemMessage = f"""You are roleplaying as a character named {ai['name']} with these traits:

                        Appearance:
                        {ai['appearance']}

                        Personality:
                        {ai['personality']}"""

        startingPrompt = f"""You enter a small party. 
                        Pick one of the following actions, formatted as valid JSON in the form \"action\": [your chosen action]
                        
                        Available actions:
                        {actions}"""

        messages_list.append([{"role": "system", "content": systemMessage}])
        messages_list[ai["id"]].append({"role": "system", "content": startingPrompt})

    actions = run_ais()

    return actions


def run_ais():
    actions = []
    for index, messages in enumerate(messages_list):
        completion = client.chat.completions.create(
            model=config.model,
            max_tokens=config.max_tokens,
            response_format={"type": "json_object"},
            messages=messages,
        )
        responseStr = completion.choices[0].message.content
        response = json.loads(responseStr)
        actions.append({"id": index, "action": response["action"]})
    return actions


test_actions = "Talk to someone, Find a place to sit, Find somewhere quiet"

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

actions = start_simulation(test_actions, test_ais)

for i in actions:
    print(i)
