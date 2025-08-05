# 🤖 hAIck: The Conversational Video Intelligence Assistant

**hAIck** is a powerful local AI assistant that lets users interact with YouTube videos through smart conversations. With transcript-aware Q&A, persistent chat history, and context-aware reasoning, hAIck helps you *understand videos without watching them end-to-end*.

Forget passive learning. Just ask, and hAIck answers. 💡

---

## 🧠 Project Overview

**hAIck** is designed to tackle a common challenge: extracting insights from long, information-dense videos.

Instead of watching the entire video or manually searching for specific parts, users can:

- 💬 Ask contextual questions about the video content.
- 📜 Receive summarized explanations based on selected depth.
- 🧠 Interact with the assistant across multiple sessions with memory and context retention.

Whether it's a lecture, tech talk, or tutorial — hAIck makes videos *interactive, searchable, and intelligent*.

---

## 🏗️ Architecture Diagram

<pre> +-------------------------+ | YouTube Video URL | +-----------+------------+ | v +-------------------------+ | YouTube Transcript API | +-----------+------------+ | v +----------------------------+ | Transcript Chunker | | - Sentence-wise (QnA) | | - Segment-wise (Summary) | +-----------+----------------+ | v +-----------------------------+ | Gemini LLM via LangChain | | - QnA Engine | | - Summary Generator | | - Memory + Context Handler | +-----------+-----------------+ | v +-----------------------------+ | Streamlit Frontend | +-----------------------------+ </pre>

---

## 🧰 Tech Stack Justification

| Layer | Tech | Why |
|------|------|-----|
| **Frontend** | Streamlit | Lightweight, easy UI framework for local demos |
| **LLM** | Gemini API (via LangChain) | Robust natural language understanding + LangChain memory modules |
| **Transcript** | YouTube Transcript API | Accesses video transcripts directly without downloads |
| **Memory** | LangChain Memory + File Loader | Maintains multi-session context with optional import support |

---

## ⚙️ Setup & Installation Instructions

> 💻 This project runs locally on Streamlit with Python 3.10+

### 1. Clone the Repo
```bash
git clone https://github.com/KingasRahd/hAIck.git
cd hAIck
2. Create and Activate a Virtual Environment
bash
Copy code
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Add Your Gemini API Key
Create a .env file in the root directory:

env
Copy code
API_KEY=your_api_key_here
5. Run the App
bash
Copy code
streamlit run app.py
🚀 Usage Instructions
🎯 What You Can Do
Input a YouTube video URL (with an available transcript)

Ask questions like:

“What is the main idea discussed?”

“Summarize the 3rd section.”

“What were the pros and cons mentioned?”

Upload previous chat sessions for seamless context carry-over

Choose summary granularity: overview or detailed

📸 Example Flow
Paste a YouTube video link

Ask: “What’s the core concept explained here?”

Ask: “Any real-life use cases mentioned?”

Continue later with session import if needed

🎥 Demo Video
Watch hAIck in action:
👉 Demo Video Placeholder – Coming Soon

🙌 Acknowledgements
LangChain

Gemini API

Streamlit

YouTube Transcript API

💡 Built with ❤️ by Sagnik for [Hackathon Name]