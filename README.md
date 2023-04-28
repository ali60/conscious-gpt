# conscious-gpt

# ChatGPT

ChatGPT is a Python script that uses OpenAI's GPT-3 natural language processing model to create a chatbot that can answer questions and generate new questions based on a summary of previous questions. The chatbot stores conversation history in a local SQLite database, allowing it to learn and improve over time.

## Prerequisites

To run ChatGPT, you will need:

- Python 3.x
- An OpenAI API key
- The `openai`, `sqlite3`, `nltk`, and `gensim` Python packages

## Getting Started

1. Clone the repository or download the `chatgpt.py` file.
2. Install the required packages using `pip`:

   ```
   pip install openai sqlite3 nltk gensim
   ```

3. Set your OpenAI API key as the value of the `openai.api_key` variable at the top of the `chatgpt.py` file.
4. Run the script using the following command:

   ```
   python chatgpt.py
   ```

5. The script will prompt you to enter questions or responses. ChatGPT will respond with a generated question or a response based on the input and the summary of previous questions stored in the database.

## How it Works

When you run ChatGPT, it connects to a local SQLite database (`chat_history.db`) that stores the conversation history. If the database does not exist, the script creates it and creates a table to store the conversation history.

The script then enters a loop, prompting the user to enter a question or response. The script retrieves all previous questions from the database and concatenates them into a single text string. It then uses the `summarize_text` function to generate a summary of the previous questions.

The `generate_question` function uses the summary text to prompt the user to generate a new question. The user's input is then passed to the `ask_gpt` function, which generates a response using the GPT-3 model.

The response is printed to the console, and the conversation is inserted into the database. If the user enters "exit", the script terminates and the database connection is closed.

## Contributing

Contributions to ChatGPT are welcome! If you find a bug or have a suggestion for an improvement, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
