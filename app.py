from flask import Flask, render_template, jsonify, request, redirect, url_for
import openai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")


app = Flask(__name__, template_folder='templates', static_folder='static')

openai.api_key = api_key

@app.route('/')
def index():
    return redirect(url_for('chat'))

@app.route('/chat', methods = ['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_input = request.form.get('message')

        try:

            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input}
                ]
            )
            response_message = response.choices[0].message.content

        except Exception as e:
            response_message = f"Fehler: {str(e)}"

        return jsonify({"response": response_message})
    return render_template('chat.html')


@app.route('/email_generator', methods=['GET', 'POST'])
def email_generator():
    if request.method == 'POST':
        email_input = request.form.get('email_input')
        bullet_points = request.form.get('bullet_points')

        prompt = f"Erstelle eine Antwort auf die folgende E-Mail:\n\n{email_input}\n\nBerücksichtige folgende Punkte: {bullet_points}"

        try:

            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for writing emails."},
                    {"role": "user", "content": prompt}
                ]
            )
            generated_response = response.choices[0].message.content
        except Exception as e:
            generated_response = f"Fehler: {str(e)}"

        return jsonify({"response": generated_response})

    return render_template('email_generator.html')

if __name__ == '__main__':
    app.run(debug=True)
