import openai
import re
import os
from database import Database

openai.api_key = os.getenv("OPENAI_API_KEY")


# this method is used to ask gpt3 for a response
def ask_gpt(prompt, temperature=0.5) -> str:
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


def get_or_save_user_name(db) -> str:
    name_row = db.get_user_name()

    if not name_row:
        user_name = input("Please enter your name: ")
        db.save_user_name(user_name)
        return user_name
    else:
        return name_row[0]


def summarize_text(text):
    prompt = "Please summarize the following text:\n" + text
    print(f"[log] summarizing text: {text}")
    summary = ask_gpt(prompt)
    return summary


def generate_question(summary) -> str:
    prompt = "Please ask a funny question based on the following summary:\n" + summary
    question = ask_gpt(prompt)
    return question


def is_statement(text) -> bool:
    prompt = f"Is the following text a question or a statement?\n{text}"
    response = ask_gpt(prompt, temperature=0.2)
    if 'statement' in response.lower():
        print(f"log: {text} is a statement")
        return True
    print(f"log: {text} is a statement")
    return False


def generate_something_for_statement(summary, gpt_question, answer) -> bool:
    prompt = f" GPT asked: {gpt_question}? :and user answered:\"{answer}\". Give follow-up information for this Conversation."
    response = ask_gpt(prompt, temperature=0.5)
    return response


def main():
    db = Database()

    user_name = get_or_save_user_name(db)
    print(f"Welcome to ChatGPT, {user_name}!")
    print("Type 'exit' to end the conversation.")

    questions = db.get_all_questions()
    questions_text = "\n".join(questions)
    summary = summarize_text(questions_text)
    print(f"[log] summary of previous questions: {summary}\n")

    gpt_question = generate_question(summary)
    print(f"{gpt_question}, {user_name}?")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        if is_statement(user_input):
            response = generate_something_for_statement(summary, gpt_question, user_input)
        else:
            response = ask_gpt(prompt=user_input)
        print("ChatGPT: " + response)
        db.save_question_and_answer(user_input, response)

    db.close()


if __name__ == '__main__':
    main()
