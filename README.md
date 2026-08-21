# Lingo Forge

Lingo Forge is an English translation application built with LangChain, Groq, and Streamlit. It provides a simple web interface for translating English text into several languages and also exposes the same translation chain through a FastAPI/LangServe API.

## Live Demo

Try the deployed Streamlit application here:

**[Open Lingo Forge](https://translator-using-genai.streamlit.app/)**

The project demonstrates:

- Calling a hosted chat model with `ChatGroq`
- Building prompts with `ChatPromptTemplate`
- Composing model and parser steps with LangChain Expression Language (LCEL)
- Creating a user interface with Streamlit
- Exposing an LCEL chain through FastAPI and LangServe
- Loading API credentials securely from environment variables

## Features

- Translate English text into French, Spanish, German, Italian, Portuguese, Hindi, Japanese, or Arabic
- Clean two-panel translation workspace
- Recent translation history during the current browser session
- Download the translated text as a `.txt` file
- Loading and error states during model requests
- Notebook demonstrating the individual LangChain steps
- FastAPI/LangServe playground and API documentation
- Uses the currently available Groq model `qwen/qwen3.6-27b`

## Project Structure

```text
.
|-- app.py                  # Streamlit frontend
|-- serve.py                # Shared LCEL chain and FastAPI/LangServe API
|-- simplellmLCEL.ipynb     # Notebook walkthrough
|-- requirements.txt        # Python dependencies
|-- .env                    # Local secrets; do not commit this file
|-- .gitignore              # Recommended before publishing to GitHub
`-- venv/                   # Local virtual environment; do not commit this folder
```

## Architecture

The translation flow is shared by the frontend and API:

```text
User input
    |
    v
ChatPromptTemplate
    |
    v
ChatGroq (qwen/qwen3.6-27b)
    |
    v
StrOutputParser
    |
    v
Translated text
```

`serve.py` defines the chain:

```python
chain = prompt_template | model | parser
```

`app.py` imports this chain and invokes it with:

```python
chain.invoke({"language": language, "text": source_text})
```

This keeps the Streamlit frontend and LangServe API on the same model and prompt configuration.

## Requirements

- Windows, macOS, or Linux
- Python 3.10 or newer
- A Groq account and API key
- Internet access for Groq API requests

## Local Setup on Windows

Open PowerShell in the project directory:

```powershell
cd "C:\Programs\Projects\Translator-From Eng to Other Using Gen AI"
```

Create a virtual environment if one does not already exist:

```powershell
python -m venv venv
```

Activate it:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Configure the Groq API Key

Create a local file named `.env` in the project root:

```env
GROQ_API_KEY=your_new_groq_api_key_here
```

Never commit `.env` to GitHub. Do not paste the key into the notebook, source code, README, screenshots, or public issue reports.

If an API key has previously been exposed, revoke it in the Groq console and create a replacement before publishing the repository.

## Run the Streamlit Frontend

With the virtual environment activated, run:

```powershell
python -m streamlit run app.py
```

Open the URL shown in the terminal. The default local address is:

```text
http://localhost:8501
```

The app opens with an English text area, a target-language selector, and a Translate button. After a successful request, the result can be downloaded as a text file.

## Run the FastAPI/LangServe API

The Streamlit frontend does not require the API server because it imports the chain directly. The API is available when you want to use the chain from another client or inspect it through LangServe.

Start the API on port 8000:

```powershell
python -m uvicorn serve:app --host 127.0.0.1 --port 8000
```

Useful URLs:

- OpenAPI documentation: `http://127.0.0.1:8000/docs`
- LangServe playground: `http://127.0.0.1:8000/translate/playground/`
- Input schema: `http://127.0.0.1:8000/translate/input_schema`
- Invoke endpoint: `http://127.0.0.1:8000/translate/invoke`

Example PowerShell request:

```powershell
$body = @{
    input = @{
        language = "French"
        text = "Hello, how are you?"
    }
} | ConvertTo-Json -Depth 4

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/translate/invoke" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

## Run the Notebook

The notebook provides a step-by-step demonstration of:

1. Loading `GROQ_API_KEY` from `.env`
2. Creating a `ChatGroq` model
3. Sending `HumanMessage` and `SystemMessage` objects
4. Parsing responses with `StrOutputParser`
5. Building a basic LCEL chain
6. Creating a reusable `ChatPromptTemplate`
7. Combining the prompt, model, and parser into a complete chain

Register the project environment as a Jupyter kernel:

```powershell
python -m ipykernel install --user --name translator-venv --display-name "Python (Translator venv)"
```

In VS Code, open `simplellmLCEL.ipynb`, select the kernel named **Python (Translator venv)**, restart the kernel, and run the cells from top to bottom.

## Publishing to GitHub

Before making the repository public, create a `.gitignore` file with at least:

```gitignore
.env
venv/
__pycache__/
*.pyc
.ipynb_checkpoints/
.streamlit/secrets.toml
```

Check that no secret is tracked:

```powershell
git status
git ls-files
```

Initialize and commit the project:

```powershell
git init
git add app.py serve.py requirements.txt README.md simplellmLCEL.ipynb .gitignore
git commit -m "Build translation app with Streamlit frontend"
```

Create an empty repository on GitHub, then connect and push it:

```powershell
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

A GitHub repository link displays the source code. It does not automatically run the application.

## Deploy with Streamlit Community Cloud

To create a live application link:

1. Push this project to GitHub.
2. Open Streamlit Community Cloud.
3. Choose **New app**.
4. Select the GitHub repository and the `main` branch.
5. Set the main file to `app.py`.
6. Open the app settings and add the `GROQ_API_KEY` secret:

    ```toml
    GROQ_API_KEY = "your_new_groq_api_key"
    ```

7. Deploy the app.

For Streamlit Cloud, the application can read the secret through an environment variable. The existing `load_dotenv()` call is harmless when `.env` is absent in the cloud environment.

The current live application is:

```text
https://translator-using-genai.streamlit.app/
```

## Security Notes

- Do not commit `.env`.
- Do not hard-code the Groq API key.
- Rotate any key that has appeared in a public repository, chat, screenshot, terminal log, or notebook output.
- Keep `venv/` out of GitHub; dependencies are recreated from `requirements.txt`.
- Treat the translation endpoint as an authenticated service before exposing it publicly. The current FastAPI app does not implement user authentication or rate limiting.
- Consider adding request limits and monitoring before production use.

## Troubleshooting

### `ModuleNotFoundError`

Make sure VS Code and the terminal are using the project environment:

```powershell
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

In a notebook, choose **Python (Translator venv)** as the kernel.

### `GROQ_API_KEY is missing`

Confirm that `.env` exists in the project root and contains:

```env
GROQ_API_KEY=your_new_groq_api_key_here
```

Restart the Streamlit app or notebook kernel after changing the key.

### Groq model `404 model_not_found`

The list of models available to a Groq account can change. The current project uses `qwen/qwen3.6-27b`. If it becomes unavailable, check the models available to your account and update the model name in both `serve.py` and the notebook.

### Streamlit does not open

Run the app explicitly from the project directory:

```powershell
.\venv\Scripts\python.exe -m streamlit run app.py
```

Then open `http://localhost:8501` manually.

## License

Add the license that matches how you want other people to use this project before publishing it publicly. If you are unsure, choose a standard open-source license and include its full text in a `LICENSE` file.
