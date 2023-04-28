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
    c.execute('''CREATE TABLE IF NOT EXISTS user_info
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT)''')
    return conn, c

# this method is used to ask gpt3 for a response
def ask_gpt(prompt, temperature=0.5)->str:
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


def get_or_save_user_name(c)->str:
    c.execute("SELECT name FROM user_info")
    name_row = c.fetchone()

    if not name_row:
        user_name = input("Please enter your name: ")
        c.execute("INSERT INTO user_info (name) VALUES (?)", (user_name,))
        return user_name
    else:
        return name_row[0]


def summarize_text(text):
    prompt = "Please summarize the following text:\n" + text
    summary = ask_gpt(prompt)
    return summary


def generate_question(summary)->str:
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
    prompt = f"this is the conversation summary with user: {summary}. The use then mentioned :{text}. Give usefull information for this topic."
    response = ask_gpt(prompt, temperature=0.5)
    return response


def main():
    conn, c = connect_to_database()
    user_name = get_or_save_user_name(c)
    conn.commit()
    print(f"Welcome to ChatGPT, {user_name}!")
    print("Type 'exit' to end the conversation.")

    c.execute("SELECT question FROM chat_history")
    rows = c.fetchall()
    questions = [row[0] for row in rows]

    questions_text = "\n".join(questions)
    summary = summarize_text(questions_text)
    print(f"summary of previous questions: {summary}\n")

    gpt_question = generate_question(summary)
    print(f"{gpt_question}, {user_name}?")

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
