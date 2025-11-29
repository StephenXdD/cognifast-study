# Pastify AI - Study Companion

**Elevator Pitch:** Turn your boring lecture notes into an interactive, AI-powered study partner.

Pastify AI transforms static PDF lecture notes into dynamic, multimodal study tools in seconds, using the high-speed Groq LPU platform.

## 🚀 Features

* **Interactive Quiz:** Generate multiple-choice quizzes of adjustable difficulty.

* **Flashcards:** Extract key concepts and definitions for quick review.

* **Mind Map:** Visualize the document's structure with a Graphviz knowledge graph.

* **Audio Summary:** Listen to concise, AI-generated summaries (British accent) on the go.

* **AI Tutor:** Chat conversationally with an AI trained exclusively on your uploaded document.

## 🛠️ Built With

| Category | Technology | Purpose | 
| ----- | ----- | ----- | 
| **Language** | Python 3 | Core logic and scripting. | 
| **Framework** | Streamlit | Frontend and application interface. | 
| **AI Platform** | Groq Cloud API | Ultra-low latency inference for all generative tasks. | 
| **LLM** | Llama 3.1 8B Instant | Content generation, quiz creation, and tutoring. | 
| **PDF Processing** | `pypdf` | Text extraction from PDF documents. | 
| **Text-to-Speech** | `gTTS` | Audio generation for summaries. | 
| **Styling** | Custom CSS | Soft Neo-Minimal theme. | 

## 📖 Project Story

### Inspiration

The inspiration for **Pastify AI** came from the need to combat passive learning inherent in traditional studying. We realized that simply reading static lecture PDFs doesn't guarantee comprehension. Our core goal became: **How can we instantly convert a static, boring PDF into an engaging, multi-modal learning experience that actively tests the user?** This led to designing a study companion that automates the tedious work (extraction, summarization) so the user can focus on high-value, active study methods.

### How we built it

Pastify AI is built on a robust architecture leveraging **Python** and **Streamlit** for the frontend, powered by the incredible speed of **Groq Cloud** for AI inference.

* **Rapid AI Processing (Groq API):** We use the `llama-3.1-8b-instant` model. The low latency of the Groq LPU™ is critical for delivering near-instant quiz and flashcard generation.

* **Structured Output Engineering:** Specialized Python functions utilize fine-tuned prompts to force the LLM to return data in strict JSON formats for predictable output.

* **Two-Page Security Model:** We implemented custom session-state management. The sensitive API Key and PDF upload are confined to the **Home Page**, while the study tools operate in a secure **Tools Page**.

* **Core Files:** The project consists of `app.py` (Streamlit logic/UI), `utils.py` (AI functions), and `styles.py` (custom CSS).

### Challenges we ran into

1. **LLM JSON Adherence:** The most frequent roadblock was ensuring the LLM reliably generated perfectly structured JSON (especially for the quiz data and initial attempts at flat keyword lists), leading to numerous parsing errors. This required explicit, restrictive prompt engineering.

2. **External Tool Fragility:** An attempt to implement a "Related Videos" feature using a non-API scraping library (`Youtube`) proved highly unreliable due to network and structural changes, forcing us to remove the feature to preserve application stability.

3. **Streamlit Layout Optimization:** We successfully overcame layout issues in the quiz module, ensuring all options and the submit button fit the screen without requiring vertical scrolling.

### What we learned

We learned that **code quality and robust parsing are paramount** when dealing with LLM-generated content. We affirmed the importance of application stability, making the decision to remove features that relied on fragile external components.

**To run this project locally:**

1. Clone the repository.

2. `pip install -r requirements.txt`

3. Set your Groq API key in the Streamlit interface.

4. `streamlit run app.py`