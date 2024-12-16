from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import re

# Initialize Flask app
app = Flask(__name__)

# Configure Gemini AI with the API key
genai.configure(api_key="AIzaSyBjqSYnsr2Le7-QgX_eoATrrQ-Y9mGNS2U")
model = genai.GenerativeModel("gemini-1.5-flash")

def format_response(content):
    """
    Format the AI's response to include:
    - New lines as <br> or <p> tags for better readability.
    - Bold text for **content**.
    - Code blocks for ```content``` with appropriate HTML tags.
    """
    # Replace line breaks
    content = content.replace('/n', '<br>')

    # Add HTML paragraphs after `.`, `?`, `!`
    content = re.sub(r'([.!?]) ', r'\1<br><br>', content)

    # Convert **text** to bold using <b> tags
    content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', content)

    # Convert ```code``` to styled code blocks
    content = re.sub(r'```(.*?)```', 
                     r'<div class="code-block"><pre>\1</pre></div>', 
                     content, 
                     flags=re.DOTALL)

    # Wrap the entire content in a <div> tag for consistency
    content = f"<div class='formatted-response'>{content}</div>"

    return content

@app.route("/")
def index():
    """Serve the chatbot HTML interface."""
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    """Handle user messages and generate responses using Gemini AI."""
    user_message = request.json.get("message")
    
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        # Generate a response from the Gemini model
        response = model.generate_content(user_message)
        bot_response = response.text

        # Format the response for HTML rendering
        formatted_response = format_response(bot_response)

        return jsonify({"response": formatted_response})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to generate response"}), 500

if __name__ == "__main__":
    app.run(debug=True)