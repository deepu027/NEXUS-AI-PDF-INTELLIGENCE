# NEXUS AI — PDF Intelligence

A Streamlit college project that extracts text from PDFs with PyMuPDF and uses Google Gemini to summarize documents and answer questions.

## Project files

- `app.py` — Streamlit frontend and dashboard
- `pdf_service.py` — PDF text extraction
- `gemini_service.py` — Gemini API integration
- `requirements.txt` — Python dependencies
- `.env.example` — environment-variable template

## Requirements

- Python 3.10 or newer
- Internet connection for Gemini API requests
- A Google Gemini API key

## Setup (Windows)

1. Extract the ZIP file.
2. Open the extracted `nexus_ai_pdf_analyzer` folder in VS Code.
3. Open the VS Code terminal.
4. Create and activate a virtual environment (recommended):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

5. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

6. Copy `.env.example` and rename the copy to `.env`.
7. Open `.env` and replace `YOUR_GEMINI_API_KEY_HERE` with your own API key.
8. Start the app:

   ```powershell
   streamlit run app.py
   ```

Streamlit will show a local address, usually http://localhost:8501.

## Setup (macOS / Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Add your API key to `.env`, then run:

```bash
streamlit run app.py
```

## Important notes

- The app reads selectable text from PDFs. Scanned/image-only PDFs need OCR, which is not included.
- Gemini features require a valid API key and internet access.
- The app sends extracted PDF text to Google's Gemini API when you request a summary or ask a question. Do not upload confidential documents unless you are allowed to share them with that service.
- The starter app passes up to 50,000 characters of extracted text to Gemini per request.
- Keep `.env` private. Do not upload it to GitHub or share your API key.

## Troubleshooting

- **`GEMINI_API_KEY is missing`:** Check that `.env` is in the same folder as `app.py`, and that the key is set.
- **Model not found / unavailable:** Set `GEMINI_MODEL` in `.env` to a model currently enabled for your Google AI API key.
- **No selectable text:** The PDF may be scanned. OCR is needed for that document.
- **Port already in use:** Run `streamlit run app.py --server.port 8502`.
