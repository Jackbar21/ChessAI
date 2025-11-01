from random import choice as random_choice

SHORT_GREETING_1 = "Hi, I'm JackBot! By default, I play at medium difficulty."
SHORT_GREETING_2 = "You can change my difficulty at any time by sending: 'easy', 'medium', or 'hard' in chat."
SHORT_GREETING_3 = "Otherwise, just type something funny. Good luck!"

GREETINGS = [SHORT_GREETING_1, SHORT_GREETING_2, SHORT_GREETING_3]

RESPONSES = [
    "Bro really said '{{text}}'. ROFLCOPTER!",
    "Do you even chess, bro?",
    "Do you think you're funny lil bro?",
    "Bruh look at this dude, username is literally {{username}}. LMFAO.",
    "Is that your move or your life plan?",
    "You call that a strategy? Cute.",
    "Wow… did you learn chess from TikTok?",
    "{{username}}, are you trying to win or just amuse me?",
    "Big brain move… said no one ever.",
    "You might want to google 'how to chess', buddy.",
    "Ok, that was… bold. Very bold.",
    "{{username}} vs logic: 0-1",
    "This game is cute. Keep trying, champ.",
    "Did you forget to move the queen or your common sense?",
    "Bro, even my cat would play better.",
]

WON_RESPONSES = [
    "LMFAO get absolutely SHREDDED, {{username}}!",
    "Haha! Checkmate, {{username}}! Better luck next time!",
    "Boom! That's how it's done, get back to school {{username}}!",
    "GG {{username}}! You fought well, but not well enough!",
    "Another one bites the dust! Sorry {{username}}, not sorry!",
    "You played like a champ, but I played like a legend!",
    "Checkmate! Maybe next time you'll think twice before challenging me, {{username}}!",
]

DRAW_RESPONSES = [
    "A draw? Pfft, I was just warming up!",
    "Well, that was anticlimactic. Rematch, {{username}}?",
    "A draw it is! But next time, I'm coming for the win!",
]

LOST_RESPONSES = [
    "Well played, {{username}}! You got me this time.",
    "Congrats {{username}}, you actually won! Don't get used to it.",
    "You got lucky this time, {{username}}! I'll be back stronger.",
    "If this was Clash Royale, I'd use the Princess Yawn emote right now.",
]


def generate_response(username: str, text: str) -> str:
    """Generate a chat response as reply to user message."""
    response_template = random_choice(RESPONSES)
    response = response_template.replace("{{username}}", username).replace(
        "{{text}}", text
    )
    return response
