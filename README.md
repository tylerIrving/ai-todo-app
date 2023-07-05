# ChatGPT-todo-app

## Overview

The ChatGPT ToDo App is a Python-based web application that assists users in managing their to-do lists. It utilizes the power of OpenAI's GPT-3.5 language model to provide help in completing the task. The app is built using the Flask web framework and employs a Redis database for persistent storage. Package management is handled through Poetry.

## Features

- Contextual Suggestions: The GPT-3.5 model provides intelligent suggestions and recommendations based on user input, making task management easier and more efficient.
- Task Management: Users can add and delete todo's using the UI.

## App Example

## Requirements

To run the App, make sure you have the following installed:

- Python 3.7 or above
- Poetry (package manager)

## Installation & Running

Clone the repository:

1. Copy code

```
git clone https://github.com/your-username/chatgpt-todo-app.git
```

2. Change into the project directory:

```
cd chatgpt-todo-app
```

3. Create .env file and add the env variables

```
OPENAI_API_KEY=""
REDIS_HOST="localhost"
REDIS_PORT=6379
REDIS_DB=0
```

3. Install dependencies using Poetry:

```
poetry install
```

4. Start poetry shell

```
poetry shell
```

5. Start the app

```
python app.py
```
