from pypdf import PdfReader
from openai import OpenAI
import json
from gtts import gTTS
import tempfile
import os


def get_openai_client(api_key):
    """Initializes and returns the OpenAI client using Groq."""
    return OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")

def extract_text_from_pdf(uploaded_file):
    """Extracts text from an uploaded PDF file."""
    try:
        reader = PdfReader(uploaded_file)
        text = "".join([page.extract_text() for page in reader.pages])
        return text
    except Exception as e:
        raise Exception(f"Error reading PDF: {e}")

def generate_quiz_content(client, text, num_q, level):
    """Generates quiz questions using the LLM."""
    prompt = f"""
    Create a {num_q}-question multiple choice quiz based on this text.
    Difficulty: {level}.
    Return ONLY a valid JSON array with this structure:
    [
        {{
            "question": "Question text?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "Option B"
        }}
    ]
    
    Text: {text[:6000]}
    """
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    data = json.loads(response.choices[0].message.content)
    
    if "quiz" in data: return data["quiz"]
    elif "questions" in data: return data["questions"]
    else: return data[list(data.keys())[0]]

def generate_flashcards_content(client, text):
    """Generates flashcards content using the LLM."""
    prompt = f"""
    Extract 6 key concepts and definitions from the text. 
    Return JSON: [{{"concept": "Term", "definition": "Meaning"}}]
    Text: {text[:6000]}
    """
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    data = json.loads(response.choices[0].message.content)
    
    if isinstance(data, list): return data
    elif "flashcards" in data: return data["flashcards"]
    elif "concepts" in data: return data["concepts"]
    else:
        first_key = list(data.keys())[0]
        if isinstance(data[first_key], list): return data[first_key]
        return []

def generate_diagram_code(client, text):
    """Generates Graphviz DOT code for a diagram."""
    prompt = f"""
    Create a Graphviz DOT code to visualize the key concepts in this text.
    Keep it simple, hierarchical, and use clean labels.
    Return ONLY the code inside a code block. Do not include markdown backticks.
    Text: {text[:6000]}
    """
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    dot_code = response.choices[0].message.content.replace("```dot", "").replace("```", "").strip()
    return dot_code

def generate_audio_summary(client, text):
    """Generates an audio summary and returns the file path and script."""
    summary_prompt = f"Summarize this text into a concise, engaging 2-minute study script suitable for listening. Be sure to not include timestamps, or any type of description of music or who is speaking such as [host]. Text: {text[:6000]}"
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": summary_prompt}]
    )
    summary_text = response.choices[0].message.content
    
    tts = gTTS(text=summary_text, lang='en', tld='co.uk')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name, summary_text

def get_chat_response(client, text, input_text):
    """Generates a chat response from the AI tutor."""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": f"You are a helpful tutor. Context: {text[:6000]}"},
            {"role": "user", "content": input_text}
        ]
    )
    return response.choices[0].message.content