# API Keys and Secrets for Beginners

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

