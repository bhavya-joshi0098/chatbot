function chatApp() {
    return {
        userMessage: '',
        messages: [], // No longer persisting messages
        sendMessage() {
            if (this.userMessage.trim() === '') return;

            // Add user message to the chat
            const userMsg = { id: Date.now(), text: this.userMessage, sender: 'user' };
            this.messages.push(userMsg);

            const userMessageCopy = this.userMessage;
            this.userMessage = ''; // Clear input field

            // Send the user message to the server
            axios.post('/api/chat', { message: userMessageCopy })
                .then(response => {
                    // Process and format chatbot response
                    const formattedResponse = this.formatChatbotResponse(response.data.response);
                    const botMsg = { id: Date.now(), text: formattedResponse, sender: 'bot' };

                    this.messages.push(botMsg);

                    // Scroll chat to the bottom
                    setTimeout(() => {
                        const chatWindow = document.getElementById('chatWindow');
                        chatWindow.scrollTop = chatWindow.scrollHeight;
                    }, 100);
                })
                .catch(error => {
                    console.error(error);
                    const errorMsg = { id: Date.now(), text: 'Error: Unable to fetch response.', sender: 'bot' };
                    this.messages.push(errorMsg);
                });
        },
        formatChatbotResponse(response) {
            /**
             * Modify the chatbot response by converting:
             * - `**bold**` to `<b>bold</b>`
             * - Triple backticks (```) to `<div class="code-block"><pre>...</pre></div>`
             * - Line breaks after `.`, `!`, `?` to `<br>` tags
             */
            // Handle bold text
            response = response.replace(/\*\*(.*?)\*\*`/g, '<b>$1</b>');

            // Handle code blocks
            response = response.replace(/```(.*?)```/gs, '<div class="code-block"><pre>$1</pre></div>');

            // Add line breaks after punctuation
            response = response.replace(/([.!?]) /g, '$1<br><br>');

            // Handle line breaks (\n)
            response = response.replace(/\n/g, '<br>');

            return response;
        }
    };
}
