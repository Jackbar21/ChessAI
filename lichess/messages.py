from random import choice as random_choice

GREETING = """
Hello {{username}}! My name is JackBot, and I'm here to roast your chess skills! 😎

You can change my bot agent at any time by sending me a chat message.
Options:
- 'agent=random' : I'll make random moves, just for fun!
- 'agent=minimax' : I'll use my brain to find the best moves.
- 'agent=negamax' : I'll use the negamax algorithm to crush you!

For example, send: 'agent=minimax'. By default, I'm set to 'minimax' mode.

Otherwise, just type something funny, and I'll respond with some savage comebacks! 😂
Good luck trying to beat me!
"""

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

WON_RESPONSES = [
    "LMFAO get absolutely SCHOOLED, {{username}}! 😂",
    "Haha! Checkmate, {{username}}! Better luck next time! 😎",
    "Boom! That's how it's done, {{username}}! 💥",
    "GG {{username}}! You fought well, but not well enough! 😜",
    "Another one bites the dust! Sorry {{username}}, not sorry! 😆",
    "You played like a champ, but I played like a legend! 😎",
    "Checkmate! Maybe next time you'll think twice before challenging me, {{username}}! 😏",
]

DRAW_RESPONSES = [
    "A draw? Pfft, I was just warming up! 😎",
    "Well, that was anticlimactic. Rematch, {{username}}? 😜",
    "A draw it is! But next time, I'm coming for the win! 😆",
]

LOST_RESPONSES = [
    "Well played, {{username}}! You got me this time.",
    "Congrats {{username}}, you actually won! Don't get used to it. 😜",
    "You got lucky this time, {{username}}! I'll be back stronger. 😎",
    "If this was Clash Royale, I'd use the Princess Yawn emote right now.",
]


def generate_response(username: str, text: str) -> str:
    """Generate a chat response as reply to user message."""
    response_template = random_choice(RESPONSES)
    response = response_template.replace("{{username}}", username).replace(
        "{{text}}", text
    )
    return response
