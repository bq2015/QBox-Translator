# QBoxTranslatorServer

A lightweight Flask-based translation connector that enables local AI-driven bilingual translation via a browser plugin. It orchestrates requests from the plugin, formats prompts for your local LLM (via Ollama or other engines), and returns professional Simplified Chinese translations without relying on cloud services.

## 🚀 Features

* **Local LLM Integration**: Connects to a locally hosted LLM API (e.g., Ollama) for private and offline translation.
* **Simple Flask API**: Exposes a single `/translate` endpoint to receive translation requests.
* **Customizable Prompts**: Optionally override default plugin prompts for better translation quality.
* **Browser Plugin Compatibility**: Works seamlessly with KISS-Translator (or similar) in Chrome and mobile browsers.
* **Lightweight & Fast**: Under 100 lines of Python code, easy to package as an executable.

## 📋 Prerequisites

* **Python 3.7+**
* **Flask**
* **Requests**
* A locally running LLM service (e.g., Ollama listening on `127.0.0.1:11434`)

## 🔧 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/QBoxTranslatorServer.git
   cd QBoxTranslatorServer
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / macOS
   venv\Scripts\activate    # Windows
   pip install -r requirements.txt
   ```

## ⚙️ Configuration & Command-Line Arguments

| Argument | Shortcut | Default     | Description                                                    |
| -------- | -------- | ----------- | -------------------------------------------------------------- |
| `--m`    | `-m`     | `""`        | Force-specify the local model name (overrides plugin `model`)  |
| `--pf`   | `-pf`    | `0`         | Whether to override plugin prompt format (`0` = no, `1` = yes) |
| `--p`    | `-p`     | `6500`      | Port on which the Flask server will listen                     |
| `--k`    | `-k`     | `qbox_qhub` | API key for request authentication                             |

**Example:**

```bash
python app.py -m "llama2" -pf 1 -p 6500 -k "my_secret_key"
```

## 🚏 Usage

1. **Start your local LLM service** (e.g., Ollama):

   ```bash
   ollama serve
   ```

2. **Run QBoxTranslatorServer**:

   ```bash
   python app.py -k "your_api_key"
   ```

3. **Configure your browser plugin** (KISS-Translator or similar):

   * Set the plugin's API endpoint to `http://<server_ip>:<port>/translate`.
   * In the plugin settings, add an `Authorization` header: `Bearer your_api_key`.

4. **Enjoy seamless local AI translation** on any English web page with real-time bilingual display!

## 📖 API Endpoint

### `POST /translate`

* **Headers**:

  * `Content-Type: application/json`
  * `Authorization: Bearer <API_KEY>`

* **Body** (JSON):

  ```json
  {
    "prompt": "<original_prompt>",
    "model": "<requested_model_name>"
  }
  ```

* **Response**:

  * Returns raw JSON from your local LLM service with the translation.
  * HTTP status codes mirror the LLM service response.

## 🛠 Development & Packaging

* To package as an executable, consider using PyInstaller:

  ```bash
  pip install pyinstaller
  pyinstaller --onefile app.py
  ```

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests on GitHub.

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.
