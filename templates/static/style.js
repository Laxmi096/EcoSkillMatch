(function () {
    const style = document.createElement("style");
    style.type = "text/css";

    style.textContent = `
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

:root {
    --primary: #10b981;
    --primary-glow: rgba(16, 185, 129, 0.4);
    --accent: #34d399;
    --bg-dark: #050a15;
    --glass: rgba(15, 23, 42, 0.6);
    --glass-border: rgba(255, 255, 255, 0.08);
    --text-main: #f8fafc;
    --text-dim: #94a3b8;
}

/* --- Smooth Cinematic Background --- */
body {
    background: radial-gradient(circle at 20% 30%, #064e3b 0%, #050a15 70%);
    background-attachment: fixed;
    min-height: 100vh;
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: var(--text-main);
    overflow-x: hidden;
}

/* --- Frosted Navigation --- */
.navbar {
    background: rgba(5, 10, 21, 0.7) !important;
    backdrop-filter: blur(20px) saturate(180%);
    border-bottom: 1px solid var(--glass-border);
    padding: 1rem 0;
}

.navbar-brand {
    font-weight: 800;
    font-size: 1.6rem;
    letter-spacing: -1px;
    background: linear-gradient(to right, #10b981, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* --- Floating Glass Cards --- */
.dashboard-card {
    background: var(--glass);
    backdrop-filter: blur(16px) saturate(120%);
    border-radius: 28px;
    border: 1px solid var(--glass-border);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    transition: all 0.5s cubic-bezier(0.23, 1, 0.32, 1);
    position: relative;
    overflow: hidden;
}

.dashboard-card::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
    transition: 0.5s;
}

.dashboard-card:hover {
    transform: translateY(-12px) scale(1.02);
    border-color: rgba(16, 185, 129, 0.5);
    box-shadow: 0 20px 40px rgba(16, 185, 129, 0.15);
}

.dashboard-card:hover::before {
    left: 100%;
}

/* --- Attractive Buttons with Inner Glow --- */
.btn-success {
    background: linear-gradient(135deg, #10b981, #059669);
    border: none;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 14px 32px;
    border-radius: 16px;
    box-shadow: 0 4px 15px var(--primary-glow);
    transition: all 0.3s ease;
}

.btn-success:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px var(--primary-glow);
    filter: brightness(1.1);
}

/* --- Neon Badges --- */
.badge {
    padding: 8px 14px;
    border-radius: 12px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

.bg-success {
    background: rgba(16, 185, 129, 0.15) !important;
    color: #34d399 !important;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.bg-danger {
    background: rgba(239, 68, 68, 0.15) !important;
    color: #f87171 !important;
    border: 1px solid rgba(239, 68, 68, 0.3);
}

/* --- Aesthetic Form Inputs --- */
.form-control {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid var(--glass-border) !important;
    color: white !important;
    border-radius: 14px !important;
    padding: 12px 18px !important;
    transition: 0.3s;
}

.form-control:focus {
    background: rgba(255, 255, 255, 0.07) !important;
    border-color: var(--primary) !important;
    box-shadow: 0 0 15px var(--primary-glow) !important;
}

/* --- Custom Scrollbar --- */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: var(--bg-dark); }
::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--primary); }

.text-gradient {
    background: linear-gradient(to right, #ffffff, #94a3b8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
`;

    document.head.appendChild(style);
})();
function toggleChat() {
    const window = document.getElementById('chat-window');
    window.classList.toggle('d-none');
}

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const msgContainer = document.getElementById('chat-messages');
    const text = input.value.trim();

    if (!text) return;

    // Append User Message
    msgContainer.innerHTML += `<div class="text-end mb-2"><span class="bg-primary px-2 py-1 rounded-3">${text}</span></div>`;
    input.value = '';

    try {
        const response = await fetch('/ai-assistant', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                message: text,
                job_context: "Sustainability Sector roles in India"
            })
        });

        const data = await response.json();
        
        // Append AI Reply
        msgContainer.innerHTML += `<div class="text-start mb-2"><span class="bg-dark border border-secondary px-2 py-1 rounded-3">${data.reply}</span></div>`;
        msgContainer.scrollTop = msgContainer.scrollHeight;
    } catch (err) {
        msgContainer.innerHTML += `<div class="text-danger small">Connection error...</div>`;
    }
}