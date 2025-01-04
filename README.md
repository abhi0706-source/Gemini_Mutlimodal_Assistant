
# ✨ **Gemini Multimodal RAG Assistant** 🌟

The **Gemini Multimodal RAG Assistant** is a cutting-edge 🛠️ Retrieval-Augmented Generation (RAG) system 🚀 powered by Gemini AI models 🤖. It offers modular agents, task orchestration, and advanced tools to deliver accurate ✅, context-aware 🧠, and structured 📊 responses to user queries. Supporting diverse functionalities 🌈 like document processing 📂, web-based content retrieval 🌐, and AI-driven query resolution 🤓, the assistant includes options for **web search answers** 🔍 and **LLM-based answers** 💡, making it a versatile solution for all information needs 📚.

---

## **Features** 🏅

### **1. Intelligent Retrieval-Augmented Generation** 🧠📚
- Answers ❓ queries based on provided contexts 📜 or documents 📝.
- Utilizes Gemini models 🌌 for generating structured 🏗️, citation-supported responses 🖋️.
- Dynamically switches 🔄 between RAG 🛠️, web search 🔍, and LLM answering modes 💡.

### **2. Multimodal Capabilities** 🖼️🔊📂
- Processes and handles various data types 📁:
  - **🎥 Video, 🎙️ Audio, 📄 PDFs, 📃 DOCX, 📊 CSV, 📝 Text files, and 🌐 Web Pages.**
- Downloads ⬇️ and processes content from URLs 🔗.
- Leverages Gemini’s chunking capabilities 🪓 to generate meaningful content segments 🧩.

### **3. Modular Agent Framework** 🤖🧩
- Implements agents tailored 🛠️ for specific roles 🎭:
  - **RAG Agent** 🛠️: Answers ❓ queries using relevant contexts 📜 with **agentic chunking** 🧩.
  - **Web Search Agent** 🔍: Retrieves information 🌐 and generates coherent responses 🖋️.
  - **Researcher Agent** 📖: Explores 🔍 technological trends 📈.
  - **Writer Agent** 🖋️: Crafts engaging 📜 narratives from technical data 💾.
- Supports role delegation 👥 and memory 🧠 for persistent context management 🗂️.

### **4. Task-Oriented Workflow** 📋✅
- Tasks designed 🛠️ with clear descriptions 📖 and expected outputs 🎯:
  - Research 📖 and report generation 🖋️.
  - Writing ✍️ industry-specific blogs 📝 or articles 📚.
  - Context-based query resolution 🧠 with citations 📜.

### **5. API-Driven Backend** 🔌
- FastAPI-based backend ⚡ to manage query resolution ❓, document embedding 📜, and context processing 🧠.
- Streamlit-based frontend 🖥️ for seamless user interaction 👩‍💻.

---

## **Architecture Overview** 🏗️

### **Core Components** 🧩
1. **Agents** 🤖 (`agents.py`):
   - Define specialized roles 🎭 for research 📖, writing ✍️, and query answering ❓.
   - Integrate tools 🛠️ for web search 🔍 and content generation 🖋️.

2. **Crew Orchestration** 👥 (`crew.py`):
   - Executes multi-agent tasks 🛠️ in sequential workflows 🔄.
   - Configures agent responsibilities 🎭 and manages outputs 📝.

3. **Tasks** 📋 (`tasks.py`):
   - Encapsulate task definitions 📖 with clear goals 🎯 and expected outputs ✅.
   - Enable asynchronous 🔄 and synchronous ⏱️ task execution 🛠️.

4. **Document Management** 📂 (`knowledge_base.py`):
   - Processes 📜 and segments documents 📝 for embedding and context retrieval 🧠.
   - Supports text 📝, PDFs 📄, DOCX 📃, CSV 📊, and other formats 🗂️.

5. **Vector Store** 🧠 (`VectorDB.py`):
   - Manages embeddings 🧩 using BERT 🌌 and ChromaDB 🛠️.
   - Facilitates fast ⚡ and accurate ✅ context retrieval 📂.

6. **Gemini Assistant** 🤖 (`gemini_assistant.py`, `assistant_v1.py`):
   - Powers AI-driven query resolution 🧠 and structured 📊 responses 🖋️.
   - Configured with custom system prompts 🛠️ for tailored answers 🎯.

---

## **Installation** 💻

### **Prerequisites** 🛠️
- 🐍 Python 3.8+
- GPU-enabled environment 🖥️ for enhanced embedding generation 🧩 (optional).

### **Setup Instructions** 📋
1. Clone the repository 📦:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   cd src
   ```

2. Install dependencies 🛠️:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables 🔑:
   - Create a `.env` file 📄 in the project root:
     ```plaintext
     GEMINI_API_KEY=<your-gemini-api-key>
     SERPER_API_KEY=<your-serper-api-key>
     ```

4. Run the FastAPI server 🚀:
   ```bash
   uvicorn response_api:app --reload
   # or
   python response_api.py
   ```

5. Launch the Streamlit interface 🖥️:
   ```bash
   streamlit run app.py
   ```

---

## **Usage** 🤓

### **Query Modes** 🔄
1. **RAG Mode** 🛠️:
   - Generates answers ❓ using document embeddings 🧠 and context 📜.
2. **LLM Answering** 🤖:
   - Provides direct responses 🖋️ using the Gemini model 🌌.
3. **Web Search Agent** 🔍:
   - Retrieves and synthesizes information 🌐 from online sources 🖋️.

### **Workflow** 🔄
1. Upload 📤 documents 📜 or provide query contexts 📂 via the Streamlit interface 🖥️.
2. Select the desired query mode 🎯.
3. View 👁️ structured 📊 answers 🖋️ with detailed citations 📜 and context 📂.

### **API Endpoints** 🔌
- **`/get-response`**: RAG-based query resolution 🛠️.
- **`/llm-response`**: Direct LLM answers 💡 from Gemini 🌌.
- **`/process-file`**: Embeds documents 📜 into the vector database 🧠.
- **`/delete-file`**: Removes embeddings 🗑️ from the database 🧠.

---

## **Supported File Types** 🗂️

| **File Type** 📂 | **Supported Actions** ✅                |
|-----------------|----------------------------------------|
| 📄 PDF         | Text extraction 🖋️ and embedding 🧠. |
| 📃 DOCX        | Processes paragraphs 📜 and content 🖋️. |
| 📊 CSV         | Converts data 📉 into readable text 🖋️. |
| 📝 Text        | Embeds plain text files 📜.             |
| 🌐 Web Pages   | Scrapes 🕸️ and processes HTML content 📜. |
| 🎥 Audio/Video | Transcribes 🎙️ and segments content 🎞️. |

---

## **Customization** ✨

### **Task Definitions** 📋
- **Research Tasks** 📖:
  - Goal 🎯: Identify technological trends 📈.
  - Output ✅: Comprehensive reports 📊 on emerging topics 🌟.
- **Writing Tasks** ✍️:
  - Goal 🎯: Create engaging 📜 industry blogs 📝.
  - Output ✅: Markdown-formatted articles 📄.
- **RAG Tasks** 🛠️:
  - Goal 🎯: Provide context-based answers 🧠 with citations 📜.
  - Output ✅: JSON-structured answers 🖋️.

### **Tool Integration** 🛠️
- Utilizes `SerperDevTool` 🔌 for live web searches 🔍.
- Modular design 🛠️ allows integration of additional tools ⚙️.

---

## **Future Enhancements** 🔮
1. Expand 🌎 multi-language support 🗣️ for agents 🤖 and tasks 📋.
2. Optimize ⚡ embeddings 🧠 using newer transformer models 🌌.
3. Introduce additional query modes 🛠️, such as real-time analytics 📈.

---

For questions ❓, contributions ✍️, or feedback 💡, feel free to contact 📩 the repository owner 👩‍💻.

---

