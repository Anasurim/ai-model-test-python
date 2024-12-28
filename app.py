from flask import Flask, render_template, jsonify, request, redirect, url_for
import openai
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

openai.api_key = "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"

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
