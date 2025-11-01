from random import choice as random_choice

RESPONSES = [
    "Bro really said '{{text}}' 🤣",
    "Do you even chess, bro?",
    "Do you think you're funny lil bro?",
    "Bruh look at this dude, username is literally {{username}}. LMFAO.",
    "Is that your move or your life plan? 😂",
    "You call that a strategy? Cute.",
    "Wow… did you learn chess from TikTok?",
    "{{username}}, are you trying to win or just amuse me?",
    "Big brain move… said no one ever.",
    "You might want to google 'how to chess', buddy.",
    "Ok, that was… bold. Very bold. 😎",
    "{{username}} vs logic: 0-1",
    "This game is cute. Keep trying, champ.",
    "Did you forget to move the queen or your common sense?",
    "Bro, even my cat would play better. 🐱",
]


def generate_response(username: str, text: str) -> str:
    response_template = random_choice(RESPONSES)
    response = response_template.replace("{{username}}", username).replace(
        "{{text}}", text
    )
    return response
