from flask import Flask, request, render_template, session, redirect, url_for
import os
import markdown
from groq import Groq

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'conversation' not in session:
        session['conversation'] = []

    if request.method == 'POST':
        user_input = request.form['user_input']
        assistant_prompt = request.form.get('assistant_prompt', '')

        if assistant_prompt:
            assistant_message = {"role": "system", "content": assistant_prompt}
            session['conversation'].append(assistant_message)
            session['assistant_prompt'] = assistant_prompt

        user_message = {"role": "user", "content": user_input}
        session['conversation'].append(user_message)

        try:
            print(session['conversation'])
            chat_completion = client.chat.completions.create(
                max_tokens=8192,
                messages=session['conversation'],
                model="llama3-70b-8192",
            )
            response_text = chat_completion.choices[0].message.content
            response = markdown.markdown(response_text, extensions=['fenced_code'])
            model_message = {"role": "assistant", "content": response}
            session['conversation'].append(model_message)
        except Exception as e:
            response = "Error connecting to the model: " + str(e)
            model_message = {"role": "assistant", "content": response}
            session['conversation'].append(model_message)

        session.modified = True
        return redirect(url_for('index'))

    return render_template('index.html', conversation=session['conversation'], assistant_prompt=session.get('assistant_prompt', 'You are a helpful assistant'))

@app.route('/reset', methods=['POST'])
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4001, debug=True)
