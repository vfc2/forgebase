class ChatInterface {
    constructor() {
        this.messagesDiv = document.getElementById('messages');
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.resetBtn = document.getElementById('resetBtn');

        this.setupEventListeners();
        this.messageInput.focus();
    }

    setupEventListeners() {
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.resetBtn.addEventListener('click', () => this.resetChat());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
    }

    addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'agent'}`;
        // Use textContent to safely set text, CSS white-space: pre-wrap will handle newlines
        messageDiv.textContent = content;
        this.messagesDiv.appendChild(messageDiv);
        this.scrollToBottom();
        return messageDiv;
    }

    scrollToBottom() {
        this.messagesDiv.scrollTop = this.messagesDiv.scrollHeight;
    }

    async sendMessage() {
        const text = this.messageInput.value.trim();
        if (!text) return;

        // Disable input during processing
        this.setInputEnabled(false);

        // Add user message
        this.addMessage(`You: ${text}`, true);
        this.messageInput.value = '';

        // Create agent message container
        const agentMessage = this.addMessage('Agent: ', false);

        try {
            const response = await fetch('/api/chat/stream', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const reader = response.body.getReader();
            let agentText = 'Agent: ';

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = new TextDecoder().decode(value);
                agentText += chunk;
                // Use textContent for safety, CSS white-space: pre-wrap will preserve newlines
                agentMessage.textContent = agentText;
                this.scrollToBottom();
            }
        } catch (error) {
            agentMessage.textContent = 'Agent: Sorry, an error occurred while processing your message.';
            console.error('Chat error:', error);
        } finally {
            this.setInputEnabled(true);
            this.messageInput.focus();
        }
    }

    async resetChat() {
        try {
            await fetch('/api/chat/reset', { method: 'POST' });
            this.messagesDiv.innerHTML = '';
            this.messageInput.focus();
        } catch (error) {
            console.error('Reset error:', error);
        }
    }

    setInputEnabled(enabled) {
        this.messageInput.disabled = !enabled;
        this.sendBtn.disabled = !enabled;
        this.resetBtn.disabled = !enabled;
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatInterface();
});
