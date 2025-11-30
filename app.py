import streamlit as st
from styles import apply_custom_css
from utils import (
    get_openai_client,
    extract_text_from_pdf,
    generate_quiz_content,
    generate_flashcards_content,
    generate_diagram_code,
    generate_audio_summary,
    get_chat_response
    # get_youtube_recommendations REMOVED
)
import os
import json

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CogniFast Study",
    page_icon="🎓",
    layout="wide"
)

# Apply Custom CSS
apply_custom_css()

# --- SESSION STATE INITIALIZATION ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'client' not in st.session_state:
    st.session_state.client = None
if 'document_text' not in st.session_state:
    st.session_state.document_text = None
if 'document_name' not in st.session_state:
    st.session_state.document_name = None

# --- PAGE FUNCTIONS ---

def render_home_page():
    """Renders the configuration page for API Key and PDF upload."""
    
    # Hide the sidebar on the home page for a cleaner look
    st.markdown("""
        <style>
        section[data-testid="stSidebar"] {
            visibility: hidden;
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.title("🎓 CogniFast Study")
    st.caption("Turn your boring lecture notes into an interactive study partner.")
    
    st.markdown("---")
    st.warning("🔑 **Step 1:** Enter your Groq API Key and upload your PDF document to begin analysis.")

    with st.form(key='config_form'):
        # API Key Input
        api_key = st.text_input("Enter Groq API Key", type="password")
        
        # PDF Upload
        uploaded_file = st.file_uploader("Upload PDF Document", type="pdf")
        
        st.markdown("<br>", unsafe_allow_html=True) 
        submit_button = st.form_submit_button(label='🚀 Analyze Document', type="primary")

    # Display settings and instructions in a box
    st.markdown("""
    <div style="padding: 15px; border: 1px solid #DADCE0; border-radius: 8px; margin-top: 30px;">
        <h4 style="color: #202124; margin-top: 0;">🌟 How to use</h4>
        <p style="color: #5F6368; line-height: 1.5;">
        1. Enter your Groq API Key.<br>
        2. Upload your PDF notes (API Key and PDF are ONLY visible here).<br>
        3. Click 'Analyze Document' to proceed to the study tools page.<br>
        <br>
        💡 **Pro Tip:** Pastify AI runs entirely on the Groq LPU™ for instant speeds.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # --- CREATOR INFO SECTION (Styled in styles.py) ---
    st.markdown("---")
    st.markdown(
        f"""
        <div class="creator-links">
            <h1><p class="main-credits">✨ Created by: **Veer Sanghvi** and **Dev Joshi**</p> </h1>
             <h1><p class="github-links"> </h1>
                <a href="https://github.com/9958ViceVortex" target="_blank">Veer Sanghvi's GitHub</a> |
                <a href="https://github.com/StephenXdD" target="_blank">Dev Joshi's GitHub</a>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    # --- END OF CREATOR INFO SECTION ---

    if submit_button:
        if not api_key:
            st.error("Please enter your Groq API Key.")
        elif not uploaded_file:
            st.error("Please upload a PDF document.")
        else:
            # Processing logic
            with st.spinner("Extracting text and preparing AI client..."):
                try:
                    # Need to read the file content twice if st.file_uploader is used
                    uploaded_file.seek(0)
                    text = extract_text_from_pdf(uploaded_file)
                    
                    client = get_openai_client(api_key)
                    
                    # Store data in session state and switch page
                    st.session_state.client = client
                    st.session_state.document_text = text
                    st.session_state.document_name = uploaded_file.name
                    st.session_state.page = 'tools'
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error processing file: {e}")

def render_tools_page():
    """Renders the main study tools and tabs."""
    client = st.session_state.client
    text = st.session_state.document_text
    doc_name = st.session_state.document_name

    # --- TOP HEADER AND HOME BUTTON ---
    col_title, col_button = st.columns([4, 1])
    with col_title:
        st.title("📚 Study Tools")
        st.caption(f"Analyzing: **{doc_name}**")
        
    with col_button:
        # Button to go back to the home page (clears core data)
        if st.button("🏠 New Document", key="home_btn", type="secondary"):
            st.session_state.page = 'home'
            st.session_state.client = None
            st.session_state.document_text = None
            st.session_state.document_name = None
            # Clear study specific keys
            for key in ["quiz_data", "flashcards", "diagram", "audio_path", "chat_history"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    # --- TABS ---
    # Removed "📺 Related Videos" tab
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Interactive Quiz", 
        "⚡ Flashcards", 
        "📊 Mind Map", 
        "🎧 Audio Summary", 
        "💬 AI Tutor"
    ])

    # --- TAB 1: INTERACTIVE QUIZ ---
    with tab1:
        col1, col2 = st.columns([1, 2.5])
        
        with col1:
            st.markdown("#### Quiz Configuration")
            num_q = st.number_input("Number of Questions", 3, 10, 5, key="num_q_input")
            level = st.select_slider("Difficulty", ["Easy", "Medium", "Hard"], key="level_slider")
            
            st.markdown("<br>", unsafe_allow_html=True) 
            
            if st.button("✨ Generate Quiz", type="primary", key="generate_quiz_tool_btn"):
                with st.spinner("Analyzing content..."):
                    try:
                        quiz_data = generate_quiz_content(client, text, num_q, level)
                        
                        st.session_state.quiz_data = quiz_data
                        st.session_state.current_question = 0
                        st.session_state.score = 0
                        st.session_state.total_questions = len(st.session_state.quiz_data)
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error: {e}")

        with col2:
            if "quiz_data" in st.session_state and st.session_state.quiz_data:
                question = st.session_state.quiz_data[0]
                
                # Progress
                q_left = len(st.session_state.quiz_data)
                total = st.session_state.total_questions
                current = total - q_left + 1
                st.caption(f"Question {current} of {total}")
                st.progress(current / total)
                
                # Question Card
                st.markdown(f"""
                <div class="question-box">
                    <h3>{question['question']}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Options (Styled as Cards via CSS)
                user_answer = st.radio(
                    "Select your answer:", 
                    question['options'], 
                    key=f"q_{current}_radio", 
                    label_visibility="collapsed"
                )
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                if st.button("Submit Answer", key=f"q_{current}_submit"):
                    correct_answer = question['answer']
                    if user_answer and (user_answer in correct_answer or correct_answer in user_answer):
                        st.toast("Correct! 🎉", icon="✅")
                        st.session_state.score += 1
                    else:
                        st.toast(f"Wrong! The answer was {correct_answer}", icon="❌")
                    
                    st.session_state.quiz_data.pop(0)
                    st.rerun()

            elif "quiz_data" in st.session_state and not st.session_state.quiz_data:
                 st.balloons()
                 
                 score = st.session_state.score
                 total = st.session_state.total_questions
                 percentage = (score / total) * 100 if total > 0 else 0
                 
                 # Determine feedback based on score
                 if percentage >= 80:
                     feedback_emoji = "🧠"
                     feedback_text = "Excellent! You've mastered these concepts."
                     color = "#10B981" # Green
                 elif percentage >= 50:
                     feedback_emoji = "💪"
                     feedback_text = "Good job! A little more practice will get you there."
                     color = "#F59E0B" # Yellow/Orange
                 else:
                     feedback_emoji = "📚"
                     feedback_text = "Keep studying! Reviewing the flashcards will help."
                     color = "#EF4444" # Red
                     
                 # NEW: Improved Score Display using Streamlit's built-in metric and custom styling
                 st.markdown(f"""
                 <div style="text-align: center; padding: 50px; background: white; border-radius: 16px; border: 1px solid #E2E8F0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                    <h2 style="color: {color}; margin-top: 0;">{feedback_emoji} Quiz Complete!</h2>
                    
                    <div style="margin-top: 20px; display: flex; justify-content: center; align-items: baseline; gap: 20px;">
                        <div style="font-size: 4rem; font-weight: 700; color: #1F2937;">
                            {score} / {total}
                        </div>
                        <div style="font-size: 2rem; color: {color}; font-weight: 500;">
                            ({percentage:.0f}%)
                        </div>
                    </div>
                    
                    <p style="font-size: 1.2rem; color: #475569; margin-top: 10px;">{feedback_text}</p>
                 </div>
                 """, unsafe_allow_html=True)
                 
                 st.markdown("<br>", unsafe_allow_html=True)
                 
                 if st.button("Start New Quiz", key="new_quiz_btn"):
                     del st.session_state.quiz_data
                     st.rerun()

            else:
                st.markdown("""
                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 300px; border: 2px dashed #DADCE0; border-radius: 16px; color: #9AA0A6;">
                    <div style="font-size: 3rem; margin-bottom: 10px;">👈</div>
                    <p style="font-weight: 500;">Configure and generate a quiz from the left panel.</p>
                </div>
                """, unsafe_allow_html=True)

    # --- TAB 2: FLASHCARDS ---
    with tab2:
        if st.button("⚡ Generate Flashcards", key="flashcard_gen_btn"):
            with st.spinner("Extracting concepts..."):
                try:
                    flashcards_data = generate_flashcards_content(client, text)
                    st.session_state.flashcards = flashcards_data
                    
                except Exception as e:
                    st.error(f"Error: {e}")

        if "flashcards" in st.session_state:
            st.markdown("<br>", unsafe_allow_html=True)
            for card in st.session_state.flashcards:
                # Styled Flashcard
                with st.expander(f"📌 {card.get('concept', 'Term')}"):
                    st.markdown(f"""
                    <div style="padding: 10px; color: #5F6368;">
                        {card.get('definition', 'Definition')}
                    </div>
                    """, unsafe_allow_html=True)

    # --- TAB 3: MIND MAP ---
    with tab3:
        st.markdown("### 🧠 Visual Knowledge Graph")
        if st.button("Generate Diagram", key="diagram_gen_btn"):
            with st.spinner("Visualizing relationships..."):
                try:
                    dot_code = generate_diagram_code(client, text)
                    st.session_state.diagram = dot_code
                except Exception as e: st.error(e)

        if "diagram" in st.session_state:
            st.graphviz_chart(st.session_state.diagram)

    # --- TAB 4: AUDIO SUMMARY ---
    with tab4:
        st.markdown("### 🎧 Podcast Mode")
        if st.button("Generate Audio Summary", key="audio_gen_btn"):
            with st.spinner("Writing script & recording..."):
                try:
                    audio_path, summary_text = generate_audio_summary(client, text)
                    st.session_state.audio_path = audio_path
                    st.session_state.audio_script = summary_text
                        
                except Exception as e: st.error(e)

        if "audio_path" in st.session_state:
            st.audio(st.session_state.audio_path)
            with st.expander("View Script"):
                st.write(st.session_state.audio_script)

    # --- TAB 5: CHAT ---
    with tab5:
        st.markdown("### 💬 Ask your AI Tutor")
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        for msg in st.session_state.chat_history:
            st.chat_message(msg["role"]).write(msg["content"])

        if input_text := st.chat_input("Ask about your document...", key="chat_input_tool"):
            st.session_state.chat_history.append({"role": "user", "content": input_text})
            st.chat_message("user").write(input_text)
            
            with st.chat_message("assistant"):
                try:
                    reply = get_chat_response(client, text, input_text)
                    st.write(reply)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"Error: {e}")

    # --- TAB 6: RELATED VIDEOS --- (DELETED)
    # The logic for Tab 6 is entirely removed as requested.


# --- MAIN APP EXECUTION ---

# Navigation Controller
if st.session_state.page == 'home':
    render_home_page()
elif st.session_state.page == 'tools':
    # Only render tools if the required data is present
    if st.session_state.client and st.session_state.document_text:
        render_tools_page()
    else:
        # Fallback if somehow they landed here without data
        st.session_state.page = 'home'
        st.rerun()

