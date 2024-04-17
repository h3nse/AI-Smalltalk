model = "gpt-3.5-turbo"
max_tokens = 100


def get_system_message(name, appearance, personality):
    systemMessage = f"""You are roleplaying as a character named {name} with these traits:

                        Appearance:
                        {appearance}

                        Personality:
                        {personality}"""
    return systemMessage
