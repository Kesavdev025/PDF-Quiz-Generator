import pdfplumber
from transformers import pipeline
import json

def extract_text(pdf_path):
    """Extract text from PDF with error handling"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = []
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text and len(page_text) > 10:
                    text.append(page_text)
            return "\n\n".join(text)
    except Exception as e:
        print(f"PDF Error: {str(e)}")
        return ""

def generate_quiz(text, num_questions=5):
    """Generate quiz questions from text"""
    if not text:
        return []

    qg = pipeline(
        "text2text-generation",
        model="valhalla/t5-base-qg-hl",
        max_length=128,
        truncation=True
    )

    qa = pipeline(
        "question-answering",
        model="bert-large-uncased-whole-word-masking-finetuned-squad"
    )

    quiz = []
    chunk_size = 1000

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        try:
            questions = qg(
                f"generate questions: {chunk}",
                num_return_sequences=3,
                do_sample=True
            )

            for result in questions:
                question = result['generated_text'].strip()
                if not question.endswith('?'):
                    question += '?'

                try:
                    answer = qa(question=question, context=chunk)
                    if answer['score'] > 0.01:
                        quiz.append({
                            "question": question,
                            "answer": answer['answer'],
                            "confidence": round(answer['score'], 2)
                        })
                except:
                    continue

                if len(quiz) >= num_questions:
                    return quiz[:num_questions]

        except Exception as e:
            print(f"Skipping chunk: {str(e)}")
            continue

    return quiz

if __name__ == "__main__":
    from google.colab import files
    import os

    print("Upload a PDF file:")
    uploaded = files.upload()

    if uploaded:
        pdf_file = next(iter(uploaded))
        text = extract_text(pdf_file)

        if text:
            quiz = generate_quiz(text)
            if quiz:
                output_file = "quiz_results.json"
                with open(output_file, 'w') as f:
                    json.dump(quiz, f, indent=2)
                files.download(output_file)
            else:
                print("Failed to generate quiz")
        else:
            print("Invalid PDF file")
    else:
        print("No file uploaded")
