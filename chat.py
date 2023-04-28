import openai
import re
import sqlite3
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def connect_to_database():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 question TEXT,
                 answer TEXT)''')
    return conn, c


def ask_gpt(prompt, temperature=0.5):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=temperature,
    )

    message = response.choices[0].text
    message = message.replace("\n", " ")
    message = re.sub(r'[^\w\s]', '', message)
    message = message.strip()
    return message


def summarize_text(text):
    prompt = "Please summarize the following text:\n" + text
    summary = ask_gpt(prompt)
    return summary


def generate_question(summary):
    prompt = "Please ask a funny question based on the following summary:\n" + summary
    question = ask_gpt(prompt)
    return question


def is_statement(text) -> bool:
    prompt = f"Is the following text a question or a statement?\n{text}"
    response = ask_gpt(prompt, temperature=0.2)
    if 'statement' in response.lower():
        print(f"{text} is a statement")
        return True
    print(f"{text} is a statement")
    return False

def generate_something_for_statement(summary, text) -> bool:
    prompt = f"this is the conversation summary with user: {text}. The use then mentioned :{text}. Generate positive information for the user."
    response = ask_gpt(prompt, temperature=0.2)
    return response

def main():
    conn, c = connect_to_database()

    print("Welcome to ChatGPT!", openai.api_key)
    print("Type 'exit' to end the conversation.")

    c.execute("SELECT question FROM chat_history")
    rows = c.fetchall()
    questions = [row[0] for row in rows]

    questions_text = "\n".join(questions)
    summary = summarize_text(questions_text)
    print('summary of previous questions: ' + summary)

    gpt_question = generate_question(summary)
    print(gpt_question+"??")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        response = ask_gpt(prompt=user_input)
        if is_statement(response):
            response = generate_something_for_statement(summary, response)
        print("ChatGPT: " + response)
        c.execute("INSERT INTO chat_history (question, answer) VALUES (?, ?)",
                  (user_input, response))
        conn.commit()

    conn.close()


if __name__ == '__main__':
    main()
