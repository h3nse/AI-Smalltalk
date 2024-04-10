from openai import OpenAI

client = OpenAI()

# The AI's chat history are stored here
messages = []


def start_simulation(actions, ais):
    startingPrompt = f"""You enter a small party. 
                    Pick one of the following actions, formatted as valid JSON in the form \"action\": [your chosen action]
                    
                    Available actions:
                    {actions}"""

    # Add the customized system message for each ai
    for ai in ais:
        systemMessage = f"""You are roleplaying as a character named {ai['name']} with these traits:

                        Appearance:
                        {ai['appearance']}

                        Personality:
                        {ai['personality']}"""

        messages.append([{"role": "system", "content": systemMessage}])

    run_ais()


def run_ais():

    pass
