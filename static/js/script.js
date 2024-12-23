const socket = io();

// DOM Elements
const loginButton = document.getElementById('loginButton');
const signupButton = document.getElementById('signupButton');
const signupConfirmButton = document.getElementById('signupConfirmButton');
const backToLoginButton = document.getElementById('backToLoginButton');
const joinButton = document.getElementById('joinButton');
const sendButton = document.getElementById('sendButton');
const messageInput = document.getElementById('messageInput');
const chatBox = document.getElementById('chatBox');
const sessionKeyInput = document.getElementById('sessionKey');
const chatHistoryDiv = document.getElementById('chat-history');
const chatSection = document.getElementById('Chat-container');
const authSection = document.getElementById('auth-section');

// User details
let username = null;
let sessionKey = null;

// Switch between login and signup forms
signupButton.addEventListener('click', () => {
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('signup-form').style.display = 'block';
});

backToLoginButton.addEventListener('click', () => {
    document.getElementById('signup-form').style.display = 'none';
    document.getElementById('login-form').style.display = 'block';
});

// Handle Signup
signupConfirmButton.addEventListener('click', () => {
    const signupUsername = document.getElementById('signupUsername').value.trim();
    const signupPassword = document.getElementById('signupPassword').value.trim();

    if (signupUsername && signupPassword) {
        fetch('/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: signupUsername, password: signupPassword }),
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('Signup successful. Please login.');
                    document.getElementById('signup-form').style.display = 'none';
                    document.getElementById('login-form').style.display = 'block';
                } else {
                    alert(data.message);
                }
            });
    } else {
        alert('Please fill all fields.');
    }
});

// Handle Login
// Handle Login
loginButton.addEventListener('click', () => {
    const loginUsername = document.getElementById('username').value.trim();
    const loginPassword = document.getElementById('password').value.trim();

    if (loginUsername && loginPassword) {
        fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: loginUsername, password: loginPassword }),
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    username = data.username;
                    authSection.style.display = 'none';
                    chatSection.style.display = 'block';
                    document.getElementById("main").classList.add("dimmed");
                    document.getElementById("Chat-container").style.display = "block";
                    loadChatHistory();
                } else {
                    alert(data.message);
                }
            });
    } else {
        alert('Please fill all fields.');
    }
});


// Fetch and Display Chat History
// Fetch and Display Chat History
function loadChatHistory(sessionKey = null) {
    const url = sessionKey
        ? `/chats/${username}?sessionKey=${sessionKey}`  // Fetch chats for specific session
        : `/chats/${username}`;                        // Fetch all user chats

    fetch(url)
        .then(response => response.json())
        .then(data => {
            chatHistoryDiv.innerHTML = '';
            if (!data.error) {
                // Display session history as buttons
                if (!sessionKey) {
                    const sessionKeys = [...new Set(data.map(chat => chat.session_key))]; // Get unique session keys
                    sessionKeys.forEach(key => {
                        const button = document.createElement('button');
                        button.textContent = `Session: ${key}`;
                        button.addEventListener('click', () => {
                            joinSession(key); // Join and continue session
                        });
                        chatHistoryDiv.appendChild(button);
                    });
                } else {
                    // Display chat messages for the session
                    data.forEach(chat => {
                        const messageElement = document.createElement('p');
                        messageElement.textContent = `${chat.username}: ${chat.message}`;
                        chatBox.appendChild(messageElement);
                    });
                }
            } else {
                chatHistoryDiv.innerHTML = '<p>No previous chats found.</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching chat history:', error);
        });
}

// Join and Continue a Session
function joinSession(key) {
    sessionKey = key;
    socket.emit('joinChat', { username, sessionKey });

    messageInput.disabled = false;
    sendButton.disabled = false;

    chatBox.innerHTML = ''; // Clear the chat box
    loadChatHistory(sessionKey); // Load the selected session's chat history
}



// Handle Joining Chat
joinButton.addEventListener('click', () => {
    sessionKey = sessionKeyInput.value.trim();

    if (sessionKey) {
        socket.emit('joinChat', { username, sessionKey });
        messageInput.disabled = false;
        sendButton.disabled = false;
        sessionKeyInput.disabled = true;
        joinButton.disabled = true;
        sessionKeyInput.value = '';

        loadChatHistory(sessionKey); // Load chat history for this session key
    } else {
        alert('Please enter a session key.');
    }
});


// Send Messages
sendButton.addEventListener('click', () => {
    const rawMessage = messageInput.value.trim();
    if (rawMessage) {
        socket.emit('chatMessage', { username, message: rawMessage, sessionKey });
        messageInput.value = '';
    }
});

// Receive Messages
socket.on('chatMessage', (data) => {
    if (data.sessionKey === sessionKey) {
        const messageElement = document.createElement('p');
        messageElement.textContent = `${data.username}: ${data.message}`;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll
    }
});
