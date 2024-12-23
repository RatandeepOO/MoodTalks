from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

word_replacements = {
    'a': '🅰',
    'b': '🅱',
    'c': '🅲',
    'd': '🅳',
    'e': '🅴',
    'f': '🅵',
    'g': '🅶',
    'h': '🅷',
    'i': '🅸',
    'j': '🅹',
    'k': '🅺',
    'l': '🅻',
    'm': '🅼',
    'n': '🅽',
    'o': '🅾',
    'p': '🅿',
    'q': '🆀',
    'r': '🆁',
    's': '🆂',
    't': '🆃',
    'u': '🆄',
    'v': '🆅',
    'w': '🆆',
    'x': '🆇',
    'y': '🆈',
    'z': '🆉',
    "happy": "😀",
    "joy": "😃",
    "smile": "😄",
    "laugh": "😊",
    "grin": "😁",
    "excited": "😆",
    "relieved": "😅",
    "laugh_cry": "😂",
    "lol": "🤣",
    "sad": "😢",
    "cry": "😭",
    "frown": "🙁",
    "unhappy": "☹️",
    "angry": "😡",
    "furious": "🤬",
    "frustrated": "😤",
    "love": "❤️",
    "heart": "💕",
    "kiss": "😘",
    "romance": "😍",
    "affection": "🥰",
    "wow": "😲",
    "surprise": "😮",
    "shock": "😯",
    "mind_blown": "🤯",
    "starstruck": "🤩",
    "hi": "👋",
    "hello": "👋",
    "bye": "👋",
    "wave": "🙋",
    "clap": "👏",
    "strong": "💪",
    "pray": "🙏",
    "dog": "🐶",
    "cat": "🐱",
    "kitten": "😺",
    "tree": "🌳",
    "plant": "🌱",
    "nature": "🌿",
    "sun": "☀️",
    "weather": "🌞",
    "moon": "🌙",
    "night": "🌚",
    "apple": "🍎",
    "fruit": "🍏",
    "pizza": "🍕",
    "burger": "🍔",
    "fries": "🍟",
    "drink": "☕",
    "coffee": "🥤",
    "beer": "🍺",
    "cake": "🎂",
    "dessert": "🍰",
    "donut": "🍩",
    "plane": "✈️",
    "flight": "🛫",
    "travel": "🛬",
    "home": "🏠",
    "car": "🚗",
    "drive": "🚙",
    "bike": "🚲",
    "game": "🎮",
    "play": "🕹️",
    "music": "🎵",
    "song": "🎶",
    "guitar": "🎸",
    "sports": "⚽",
    "basketball": "🏀",
    "football": "🏈",
    "tennis": "🎾",
    "star": "⭐",
    "shine": "🌟",
    "sparkle": "✨",
    "fire": "🔥",
    "yes": "✅",
    "check": "✔️",
    "man": "👨",
    "woman": "👩",
    "boy": "👦",
    "girl": "👧",
    "child": "🧒",
    "baby": "👶",
    "old_man": "👴",
    "old_woman": "👵",
    "nerd": "🤓",
    "teacher": "🧑‍🏫",
    "student": "🧑‍🎓",
    "doctor": "🧑‍⚕️",
    "artist": "🧑‍🎨",
    "astronaut": "🧑‍🚀",
    "police": "👮",
    "chef": "🧑‍🍳",
    "worker": "👷",
    "judge": "🧑‍⚖️",
    "farmer": "🧑‍🌾",
    "technologist": "🧑‍💻",
    "singer": "🧑‍🎤",
    "firefighter": "🧑‍🚒",
    "pilot": "🧑‍✈️",
    "dancer": "💃",
    "builder": "👷",
    "superhero": "🦸",
    "villain": "🦹",
    "king": "🤴",
    "queen": "👸",
    "prince": "👑",
    "princess": "👑",
    "family": "👨‍👩‍👧‍👦",
    "friend": "🧑‍🤝‍🧑",
    "couple": "👫",
    "brother": "👦",
    "bro": "👦",
    "sister": "👧",
    "parent": "👨‍👩‍👧",
        "india": "🇮🇳",
    "usa": "🇺🇸",
    "uk": "🇬🇧",
    "france": "🇫🇷",
    "germany": "🇩🇪",
    "canada": "🇨🇦",
    "japan": "🇯🇵",
    "china": "🇨🇳",
    "brazil": "🇧🇷",
    "russia": "🇷🇺",
    "italy": "🇮🇹",
    "spain": "🇪🇸",
    "mexico": "🇲🇽",
    "south_africa": "🇿🇦",
    "australia": "🇦🇺",
    "south_korea": "🇰🇷",
    "saudi_arabia": "🇸🇦",
    "argentina": "🇦🇷",
    "nigeria": "🇳🇬",
    "new_zealand": "🇳🇿",
        "christmas": "🎄",
    "new_year": "🎆",
    "halloween": "🎃",
    "easter": "🐇",
    "thanksgiving": "🦃",
    "diwali": "🪔",
    "holi": "🌈",
    "eid": "🕌",
    "hanukkah": "🕎",
    "summer": "☀️",
    "winter": "❄️",
    "autumn": "🍂",
    "spring": "🌸",
    "birthday": "🎂",
    "wedding": "💍",
    "valentine": "💝",
    "fireworks": "🎇",
    "snowman": "☃️",
    "umbrella": "☂️",
    "up": "⬆️",
    "down": "⬇️",
    "left": "⬅️",
    "right": "➡️",
    "north": "🧭",
    "south": "🧭",
    "east": "🧭",
    "west": "🧭",
    "northeast": "↗️",
    "northwest": "↖️",
    "southeast": "↘️",
    "southwest": "↙️",
    "u_turn": "↩️",
    "loop": "🔄",
    "next": "⏭️",
    "previous": "⏮️",
    "stop": "🛑",
    "what": "🫴🏼",
    "what's": "🫴🏼",
    "whats": "🫴🏼",
    "doing yoga" : "🧎🏼‍♀️",
    "why": "🤔",
    "how": "🧐",
    "where": "❓",
    "who": "👤",
    "when": "⏰",
    "which": "🤷",
    "maybe": "🤷‍♂️",
    "unknown": "❔",
    "confused": "😕",
    "doubt": "🤨",
    "run": "🏃",
    "walk": "🚶",
    "jump": "🤾",
    "dance": "💃",
    "swim": "🏊",
    "fly": "🛫",
    "sleep": "😴",
    "eat": "🍴",
    "drink": "🥤",
    "read": "📖",
    "write": "✍️",
    "play": "🎮",
    "sing": "🎤",
    "clap": "👏",
    "think": "🤔",
    "talk": "🗣️",
    "listen": "👂",
    "look": "👀",
    "watch": "📺",
    "study": "📚",
    "teach": "🧑‍🏫",
    "work": "💻",
    "build": "👷",
    "cook": "🧑‍🍳",
    "clean": "🧹",
    "write": "✍️",
    "paint": "🎨",
    "travel": "🌍",
    "drive": "🚗",
    "bike": "🚲",
    "ride": "🏇",
    "throw": "🤾",
    "catch": "🤲",
    "run_fast": "🏃‍♂️",
    "love": "❤️",
    "hug": "🤗",
    "hi": "👋",
    "hello": "👋",
    "bye": "👋",
    "wave": "🙋",
    "clap": "👏",
    "strong": "💪",
    "pray": "🙏",
    "dog": "🐶",
    "cat": "🐱",
    "kitten": "😺",
    "tree": "🌳",
    "plant": "🌱",
    "nature": "🌿",
    "sun": "☀️",
    "weather": "🌞",
    "moon": "🌙",
    "night": "🌚",
    "apple": "🍎",
    "fruit": "🍏",
    "pizza": "🍕",
    "burger": "🍔",
    "fries": "🍟",
    "drink": "☕",
    "coffee": "🥤",
    "beer": "🍺",
    "cake": "🎂",
    "dessert": "🍰",
    "donut": "🍩",
    "plane": "✈️",
    "flight": "🛫",
    "travel": "🛬",
    "home": "🏠",
    "car": "🚗",
    "drive": "🚙",
    "bike": "🚲",
    "game": "🎮",
    "play": "🕹️",
    "goodnight":"🛌🏼💤🌃🌑🌌",
    "goodmorning":"🌅",
    "sun":"☀️",
    "music": "🎵",
    "song": "🎶",
    "guitar": "🎸",
    "sports": "⚽",
    "basketball": "🏀",
    "football": "🏈",
    "tennis": "🎾",
    "star": "⭐",
    "shine": "🌟",
    "sparkle": "✨",
    "fire": "🔥",
    "yes": "✅",
    "check": "✔️",
    "man": "👨",
    "woman": "👩",
    "boy": "👦",
    "girl": "👧",
    "child": "🧒",
    "baby": "👶",
    "old_man": "👴",
    "old_woman": "👵",
    "nerd": "🤓",
    "teacher": "🧑‍🏫",
    "student": "🧑‍🎓",
    "doctor": "🧑‍⚕️",
    "artist": "🧑‍🎨",
    "astronaut": "🧑‍🚀",
    "police": "👮",
    "chef": "🧑‍🍳",
    "worker": "👷",
    "judge": "🧑‍⚖️",
    "farmer": "🧑‍🌾",
    "technologist": "🧑‍💻",
    "singer": "🧑‍🎤",
    "firefighter": "🧑‍🚒",
    "pilot": "🧑‍✈️",
    "dancer": "💃",
    "builder": "👷",
    "superhero": "🦸",
    "villain": "🦹",
    "king": "🤴",
    "queen": "👸",
    "prince": "👑",
    "princess": "👑",
    "family": "👨‍👩‍👧‍👦",
    "friend": "🧑‍🤝‍🧑",
    "couple": "👫",
    "brother": "👦",
    "sister": "👧",
    "parent": "👨‍👩‍👧",
    "india": "🇮🇳",
    "usa": "🇺🇸",
    "uk": "🇬🇧",
    "france": "🇫🇷",
    "germany": "🇩🇪",
    "canada": "🇨🇦",
    "japan": "🇯🇵",
    "china": "🇨🇳",
    "brazil": "🇧🇷",
    "russia": "🇷🇺",
    "italy": "🇮🇹",
    "spain": "🇪🇸",
    "mexico": "🇲🇽",
    "south_africa": "🇿🇦",
    "australia": "🇦🇺",
    "south_korea": "🇰🇷",
    "saudi_arabia": "🇸🇦",
    "argentina": "🇦🇷",
    "nigeria": "🇳🇬",
    "new_zealand": "🇳🇿",
    "christmas": "🎄",
    "new_year": "🎆",
    "halloween": "🎃",
    "easter": "🐇",
    "thanksgiving": "🦃",
    "diwali": "🪔",
    "holi": "🌈",
    "eid": "🕌",
    "hanukkah": "🕎",
    "summer": "☀️",
    "winter": "❄️",
    "autumn": "🍂",
    "spring": "🌸",
    "birthday": "🎂",
    "wedding": "💍",
    "valentine": "💝",
    "party": "🎉 🪩",
    "fireworks": "🎇",
    "snowman": "☃️",
    "umbrella": "☂️",
    "up": "⬆️",
    "down": "⬇️",
    "left": "⬅️",
    "right": "➡️",
    "north": "🧭",
    "south": "🧭",
    "east": "🧭",
    "west": "🧭",
    "northeast": "↗️",
    "northwest": "↖️",
    "southeast": "↘️",
    "southwest": "↙️",
    "busy": "🏃",
    "help": "🆘",
    "danger": "⚠️",
    "emergency": "🚨",
    "call": "📞",
    "message": "💬",
    "post": "📬",
    "write": "📝",
    "read": "📖",
    "study": "📚",
    "learn": "🧑‍🎓",
    "teach": "👨‍🏫",
    "build": "🏗️",
    "create": "🛠️",
    "design": "🎨",
    "draw": "✏️",
    "paint": "🖌️",
    "photograph": "📸",
    "program": "💻",
    "develop": "🖥️",
    "research": "🔬",
    "work": "💼",
    "play_game": "🎮",
    "watch_movie": "🎬",
    "read_book": "📚",
    "travel": "🛫",
    "shop": "🛍️",
    "eat": "🍽️",
    "drink": "🥤",
    "sleep": "😴",
    "wake_up": "⏰",
    "run": "🏃",
    "walking": "🚶",
    "jump": "🤸",
    "climb": "🧗",
    "dance": "💃",
    "sing": "🎤",
    "play_music": "🎵",
    "speak": "🗣️",
    "talk": "💬",
    "stop": "⏹️",
    "you":"🫵",
    "go": "🏃",
    "going": "🏃",
    "move": "🏃",
    "enter": "🚪",
    "exit": "🚪",
    "leave": "👋",
    "arrive": "🚗",
    "start": "🏁",
    "finish": "🏁",
    "help": "🆘",
    "fix": "🔧",
    "repair": "🔨",
    "break": "🔨",
    "fall": "⛷️",
    "catch": "🎣",
    "throw": "🤾",
    "teach": "📚",
    "learn": "🧑‍🎓",
    "work_on": "💻",
    "sleep": "😴",
    "running": "🏃",
    "working": "💼",
    "eating": "🍽️",
    "drinking": "🥤",
    "playing": "🎮",
    "watching": "🎬",
    "reading": "📖",
    "studying": "📚",
    "teaching": "👨‍🏫",
    "building": "🏗️",
    "creating": "🛠️",
    "designing": "🎨",
    "drawing": "✏️",
    "photographing": "📸",
    "programming": "💻",
    "developing": "🖥️",
    "researching": "🔬",
    "travelling": "🛫",
    "shopping": "🛍️",
    "sleeping": "💤",
    "climbing": "🧗",
    "dancing": "💃",
    "singing": "🎤",
    "talking": "💬",
    "moving": "🏃",
    "entering": "🚪",
    "exiting": "🚪",
    "leaving": "👋",
    "arriving": "🚗",
    "starting": "🏁",
    "finishing": "🏁",   
    ',': '🔸',
    '.': '⚫',
    '"': '❝❞',
    "'": '❛❜',
    '/': '➗',
    '?': '❓',
    '[': '🗂️',
    ']': '📚',
    '{': '📂',
    '}': '📁',
    '=': '➖',
    '+': '➕',
    '-': '➖',
    '_': '⏤',
    '*': '✳️',
    '&': '🔗',
    '%': '💯',
    '$': '💵',
    '@': '📧',
    '!': '❗',
    "call":"🤙",
    "win":"✌️",
    "victory" : "✌️",
    '~': '🌊',
    '`': '〽️',
    "goal":"🎯",
    "target":"🎯",
    "are":"🆁"
}

# Store users by session key
sessions = {}

# Database setup
DATABASE = 'chat_app.db'

# Connect to the database
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Access rows as dictionaries
    return conn

# Initialize the database
def init_db():
    with get_db() as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            session_key TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')

# Initialize DB on app start
init_db()

# Routes

# Serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# User Signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Username and password are required.'}), 400

    hashed_password = generate_password_hash(password)
    try:
        with get_db() as db:
            db.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, hashed_password)
            )
        return jsonify({'status': 'success', 'message': 'Signup successful.'})
    except sqlite3.IntegrityError:
        return jsonify({'status': 'error', 'message': 'Username already exists.'}), 400

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    with get_db() as db:
        user = db.execute(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        ).fetchone()

        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return jsonify({'status': 'success', 'message': 'Login successful.', 'username': username})
        else:
            return jsonify({'status': 'error', 'message': 'Invalid username or password.'}), 401

# Fetch chat history for a user and session key
@app.route('/chats/<username>', methods=['GET'])
def get_chats(username):
    session_key = request.args.get('sessionKey', None)  # Optional: Use sessionKey if provided
    with get_db() as db:
        if session_key:
            chats = db.execute(
                'SELECT username, message, timestamp FROM messages WHERE username = ? AND session_key = ? ORDER BY timestamp',
                (username, session_key)
            ).fetchall()
        else:
            chats = db.execute(
                'SELECT username, message, timestamp FROM messages WHERE username = ? ORDER BY timestamp',
                (username,)
            ).fetchall()

    if chats:
        return jsonify([dict(chat) for chat in chats])
    else:
        return jsonify({'error': 'No chat history found.'}), 404

@app.route('/sessions/<username>', methods=['GET'])
def get_user_sessions(username):
    """Fetch all session keys associated with a user."""
    with get_db() as db:
        sessions = db.execute(
            'SELECT DISTINCT session_key FROM messages WHERE username = ?',
            (username,)
        ).fetchall()
    
    if sessions:
        return jsonify([session['session_key'] for session in sessions])
    else:
        return jsonify({'error': 'No sessions found.'}), 404


# WebSocket Events

# Handle real-time chat messages
# Handle real-time chat messages
@socketio.on('chatMessage')
def handle_chat_message(data):
    username = data.get('username', 'Anonymous')
    raw_message = data.get('message', '')
    session_key = data.get('sessionKey')

    # Replace words in the message
    words = raw_message.split(" ")
    processed_message = " ".join([word_replacements.get(word.lower(), word) for word in words])

    # Save message to the database
    with get_db() as db:
        db.execute(
            'INSERT INTO messages (username, session_key, message) VALUES (?, ?, ?)',
            (username, session_key, processed_message)
        )

    # Broadcast the message to all users in the same session key
    if session_key in sessions:
        for user_socket in sessions[session_key]:
            emit('chatMessage', {
                'username': username,
                'message': processed_message,
                'sessionKey': session_key
            }, room=user_socket)

# Handle user joining a chat with a session key
@socketio.on('joinChat')
def handle_join_chat(data):
    username = data.get('username')
    session_key = data.get('sessionKey')
    user_socket = request.sid  # Get the user's socket ID

    # Add the user to the session's user list
    if session_key not in sessions:
        sessions[session_key] = []

    sessions[session_key].append(user_socket)

    print(f"{username} joined session {session_key}")

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port=5000)
