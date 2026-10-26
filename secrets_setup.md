# API Keys and Secrets for Beginners

## Do you need an API key for this assignment?

Based on the ad-optimization rubric, no API key is required. The rubric grades the CSV, performance calculations, budget decisions, guardrails, decision logs, baseline comparison, scaling note, and presentation. This project therefore uses a transparent Python decision agent that runs without an LLM or paid API.

The customer-service starter code is a separate example. It uses Azure OpenAI and therefore needs a model API key. The starter code does not automatically become a requirement for the ad-optimization assignment.

## If your instructor specifically requires an LLM key

Use one secret name consistently, such as `OPENAI_API_KEY`.

### GitHub Codespaces

1. Open GitHub and select your profile picture.
2. Choose **Settings**.
3. Under **Code, planning, and automation**, choose **Codespaces**.
4. Under **Codespaces secrets**, choose **New secret**.
5. Name the secret `OPENAI_API_KEY` and paste the key into **Value**.
6. Give access only to the repository for this assignment.
7. Choose **Add secret**.
8. Stop and restart the Codespace if it was already open.

GitHub exposes the secret to the Codespace as an environment variable. In Python, code can read it with:

```python
import os
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not available")
```

Never print the key, put it in a notebook cell, or commit a `.env` file.

### Google Colab

1. Open the notebook in Colab.
2. Click the key icon in the left sidebar.
3. Choose **Add new secret**.
4. Name it `OPENAI_API_KEY`.
5. Paste the key and enable notebook access.

Then load it without displaying it:

```python
from google.colab import userdata
api_key = userdata.get("OPENAI_API_KEY")
```

If you are not using an LLM, leave the secret unset and run the API-free version supplied in this project.

## Important warning about the supplied starter files

The supplied notebook includes a real-looking Azure key directly in code. Do not use or upload that value. If it belongs to your instructor or school, the owner should rotate or revoke it. A key that appears in a shared file should be treated as exposed.
