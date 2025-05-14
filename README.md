# 📘 AI-Based Quiz Generator from PDF

This tool allows you to upload a textbook or document in PDF format and automatically generate quiz questions using AI (NLP models from HuggingFace Transformers).

## 🚀 Features

- Extracts text from uploaded PDFs.
- Uses `valhalla/t5-base-qg-hl` to generate questions.
- Uses `bert-large-uncased` for answering those questions from the context.
- Outputs a JSON file with questions, answers, and confidence scores.

## 🛠️ How to Use

### 1. Google Colab (Recommended)

Upload this code to a Colab notebook and run the script. Upload your PDF when prompted.

### 2. Requirements

Install the dependencies using:

```bash
pip install -r requirements.txt
```

### 3. Run the script

```bash
python quiz_generator.py
```

> Ensure you're using it in Google Colab or a notebook that supports `files.upload()` and `files.download()`.

## 📦 Output Format

A JSON file like:

```json
[
  {
    "question": "What is the definition of health literacy?",
    "answer": "The ability to understand and use health information",
    "confidence": 0.87
  }
]
```

## 🤖 Models Used

- **Question Generator**: `valhalla/t5-base-qg-hl`
- **Answering Model**: `bert-large-uncased-whole-word-masking-finetuned-squad`

## 📜 License

MIT License
