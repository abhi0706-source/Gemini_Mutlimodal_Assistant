# import json
# import os
# import re
# import time
# from pathlib import Path
# from typing import Dict, List

# import requests
# import streamlit as st


# def extract_and_verify_url(string):
#     """Extract the URL from the string and verify if it points to content."""
#     url_pattern = re.compile(
#         r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
#     )
#     match = url_pattern.search(string)
#     if match:
#         url = match.group()
#         try:
#             response = requests.head(url, allow_redirects=True, timeout=5)
#             if response.status_code == 200:
#                 return {
#                     "url": url,
#                     "status": "Valid and content exists",
#                     "status_code": 200,
#                 }
#             else:
#                 return {
#                     "url": url,
#                     "status": f"Invalid (HTTP {response.status_code})",
#                     "status_code": response.status_code,
#                 }
#         except requests.RequestException as e:
#             return {"url": url, "status": f"Error: {e}"}
#     return {"url": "", "status": "No URL found"}


# def stream_data(data_val):
#     for word in data_val.split(" "):
#         yield word + " "
#         time.sleep(0.02)


# def list_files_in_directory(directory):
#     """List all files in the given directory."""
#     try:
#         return os.listdir(directory)
#     except FileNotFoundError:
#         return []


# def save_uploaded_file(uploaded_file, directory):
#     """Save the uploaded file to the specified directory."""
#     with open(os.path.join(directory, uploaded_file.name), "wb") as f:
#         f.write(uploaded_file.getbuffer())

#         return os.path.join(directory, uploaded_file.name)


# def call_rag_api(
#     query: str,
#     url: str,
#     is_uploaded: bool = False,
# ) -> Dict:
#     """Call the RAG API and get a response."""
#     endpoint = f"http://127.0.0.1:8000/get-response"
#     payload = {"query": query, "is_uploaded": is_uploaded, "url": url}

#     try:
#         response = requests.post(endpoint, json=payload)
#         response.raise_for_status()
#         result = response.json()
#         print(type(result))
#         print(result)
#         return {
#             "status": "success",
#             "response": result["response"],
#             "context": result["context"],
#             "citations": result["citations"],
#         }
#     except requests.exceptions.RequestException as e:
#         return {"status": "error", "message": str(e)}


# # Main Streamlit app
# def main():
#     st.title("🤖 RAG Chat Assistant")

#     # Sidebar inputs and actions
#     with st.sidebar:
#         st.header("📚 Document Control")

#         # Input directory
#         directory = st.text_input("Enter the directory path:", value="data")

#         # Ensure directory exists
#         Path(directory).mkdir(parents=True, exist_ok=True)

#         # Display files in the directory
#         st.subheader("Files in Directory")
#         files = list_files_in_directory(directory)
#         if files:
#             st.write(files)
#         else:
#             st.write("No files found.")

#         # Upload file
#         st.subheader("Upload a File")
#         uploaded_file = st.file_uploader(
#             "Choose a file", type=["txt", "pdf", "doc", "docx", "mp3", "mp4"]
#         )
#         if uploaded_file:
#             file_path = save_uploaded_file(uploaded_file, directory)
#             with st.spinner:
#                 endpoint = f"http://127.0.0.1:8000/process-file"
#                 payload = {"file_path": file_path}
#                 result = requests.post(endpoint, json=payload)
#                 st.success(result["response"])
#             st.success(f"File '{uploaded_file.name}' uploaded successfully!")

#         # Delete a file
#         st.subheader("Delete a File")
#         if files:
#             file_to_delete = st.selectbox("Select a file to delete:", options=files)
#             if st.button("Delete File"):
#                 try:
#                     os.remove(os.path.join(directory, file_to_delete))
#                     st.success(f"File '{file_to_delete}' deleted successfully!")
#                 except Exception as e:
#                     st.error(f"Error deleting file: {e}")

#         # Chat system status
#         st.divider()
#         st.markdown("### System Status")
#         if uploaded_file:
#             st.success("Document loaded")
#         else:
#             st.info("No document uploaded")

#     # Initialize chat history
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # Display chat messages in streaming manner
#     chat_placeholder = st.container()

#     for message in st.session_state.messages:
#         with chat_placeholder.container():
#             with st.chat_message(message["role"]):
#                 st.markdown(message["content"])
#                 if message["role"] == "assistant" and "context" in message:
#                     with st.expander("View source context"):
#                         st.info(message["context"])

#     # Chat input
#     if prompt := st.chat_input("Ask me anything about your documents..."):
#         res = extract_and_verify_url(prompt)
#         print(res)
#         if res["url"] != None:
#             print(res["url"])
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with chat_placeholder.container():
#             with st.chat_message("user"):
#                 st.markdown(prompt)

#         with chat_placeholder.container():
#             with st.chat_message("assistant"):
#                 with st.spinner("Thinking..."):
#                     result = call_rag_api(
#                         url=res["url"],
#                         query=prompt,
#                         is_uploaded=uploaded_file is not None,
#                     )

#                     if result["status"] == "success":

#                         response_content = result["response"]
#                         context = result["context"]
#                         citations = result["citations"]

#                         # st.markdown(response_content)
#                         st.write_stream(stream_data(response_content))
#                         with st.expander("View source context"):
#                             st.json(citations)

#                         st.session_state.messages.append(
#                             {
#                                 "role": "assistant",
#                                 "content": response_content,
#                                 "context": context,
#                                 "citations": citations,
#                             }
#                         )
#                     else:
#                         st.error(
#                             f"Error: {result.get('message', 'Unknown error occurred')}"
#                         )


# if __name__ == "__main__":
#     main()


import json
import os
import re
import time
from pathlib import Path
from typing import Dict, List

import requests
import streamlit as st
from streamlit_js_eval import streamlit_js_eval


def extract_and_verify_url(string):
    """Extract the URL from the string and verify if it points to content."""
    url_pattern = re.compile(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    )
    match = url_pattern.search(string)
    if match:
        url = match.group()
        try:
            response = requests.head(url, allow_redirects=True, timeout=5)
            if response.status_code == 200:
                return {
                    "url": url,
                    "status": "Valid and content exists",
                    "status_code": 200,
                }
            else:
                return {
                    "url": url,
                    "status": f"Invalid (HTTP {response.status_code})",
                    "status_code": response.status_code,
                }
        except requests.RequestException as e:
            return {"url": url, "status": f"Error: {e}"}
    return {"url": "", "status": "No URL found"}


def stream_data(data_val):
    for word in data_val.split(" "):
        yield word + " "
        time.sleep(0.02)


def list_files_in_directory(directory):
    """List all files in the given directory."""
    try:
        return os.listdir(directory)
    except FileNotFoundError:
        return []


def save_uploaded_file(uploaded_file, directory):
    """Save the uploaded file to the specified directory."""
    with open(os.path.join(directory, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
        return os.path.join(directory, uploaded_file.name)


def call_rag_api(query: str, url: str, is_uploaded: bool = False) -> Dict:
    """Call the RAG API and get a response."""
    endpoint = f"http://127.0.0.1:8000/get-response"
    payload = {"query": query, "is_uploaded": is_uploaded, "url": url}

    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        result = response.json()
        return {
            "status": "success",
            "response": result["response"],
            "context": result["context"],
            "citations": result["citations"],
        }
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}


def call_llm_api(query: str) -> Dict:
    """Call the LLM API for answering questions."""
    endpoint = f"http://127.0.0.1:8000/llm-response"
    payload = {"query": query}

    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        result = response.json()
        return {"status": "success", "response": result["response"]}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}


# Main Streamlit app
def main():
    st.title("🤖 Multi-Functional Chat Assistant")

    # Sidebar inputs and actions
    with st.sidebar:

        # Chat functionality selection
        mode = st.radio("Select Mode:", ["LLM Answering", "Web Search Agent", "RAG"])

        st.header("📂 Document Control")

        # Input directory
        directory = st.text_input("Enter the directory path:", value="data")

        # Ensure directory exists
        Path(directory).mkdir(parents=True, exist_ok=True)

        # Display files in the directory
        st.subheader("Files in Directory")
        files = list_files_in_directory(directory)
        if files:
            st.write(files)
        else:
            st.write("No files found.")

        # Upload file
        st.subheader("Upload a File")
        uploaded_file = st.file_uploader(
            "Choose a file", type=["txt", "pdf", "doc", "docx", "mp3", "mp4"]
        )
        if uploaded_file:
            file_path = save_uploaded_file(uploaded_file, directory)
            endpoint = f"http://127.0.0.1:8000/process-file"
            payload = {"file_path": file_path}

            with st.spinner("File is in process..."):
                response = requests.post(endpoint, json=payload)

            st.success(f"File '{uploaded_file.name}' uploaded successfully!")
            time.sleep(3)
            streamlit_js_eval(js_expressions="parent.window.location.reload()")

        # Delete a file
        st.subheader("Delete a File")
        if files:
            file_to_delete = st.selectbox("Select a file to delete:", options=files)
            if st.button("Delete File"):
                try:
                    payload = {"file_path": file_to_delete}
                    endpoint = f"http://127.0.0.1:8000/delete-file"

                    with st.spinner("File is deleting..."):
                        response = requests.post(endpoint, json=payload)
                        os.remove(os.path.join(directory, file_to_delete))

                    st.success(f"File '{file_to_delete}' deleted successfully!")
                    time.sleep(3)
                    streamlit_js_eval(js_expressions="parent.window.location.reload()")
                except Exception as e:
                    st.error(f"Error deleting file: {e}")

        # Chat system status
        st.divider()
        st.markdown("### System Status")
        if uploaded_file:
            st.success("Document loaded")
        else:
            st.info("No document uploaded")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages in streaming manner
    chat_placeholder = st.container()

    for message in st.session_state.messages:
        with chat_placeholder.container():
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # # Chat functionality selection
    # mode = st.radio("Select Mode:", ["LLM Answering", "Web Search Agent", "RAG"])

    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_placeholder.container():
            with st.chat_message("user"):
                st.markdown(prompt)

        with chat_placeholder.container():
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    citations = []
                    if mode == "LLM Answering":
                        result = call_llm_api(prompt)
                        if result["status"] == "success":
                            response_content = result.get("response", "")
                            st.write_stream(stream_data(response_content))

                            st.session_state.messages.append(
                                {"role": "assistant", "content": response_content}
                            )

                        else:
                            st.error(
                                f"Error: {result.get('message', 'Unknown error occurred')}"
                            )
                    elif mode == "Web Search Agent":
                        res = extract_and_verify_url(prompt)
                        result = call_rag_api(
                            url=res.get("url", ""),
                            query=prompt,
                            is_uploaded=uploaded_file is not None,
                        )
                        if result["status"] == "success":

                            response_content = result["response"]
                            context = result["context"]
                            citations = result["citations"]

                            # st.markdown(response_content)
                            st.write_stream(stream_data(response_content))
                            # with st.expander("View source context"):
                            #     st.json(citations)

                            st.session_state.messages.append(
                                {
                                    "role": "assistant",
                                    "content": response_content,
                                    "context": context,
                                    "citations": citations,
                                }
                            )
                        else:
                            st.error(
                                f"Error: {result.get('message', 'Unknown error occurred')}"
                            )

                    elif mode == "RAG":
                        res = extract_and_verify_url(prompt)
                        result = call_rag_api(
                            url="None",
                            query=prompt,
                            is_uploaded=uploaded_file is not None,
                        )

                        if result["status"] == "success":

                            response_content = result["response"]
                            context = result["context"]
                            citations = result["citations"]

                            # st.markdown(response_content)
                            st.write_stream(stream_data(response_content))
                            # with st.expander("View source context"):
                            #     st.json(citations)

                            st.session_state.messages.append(
                                {
                                    "role": "assistant",
                                    "content": response_content,
                                    "context": context,
                                    "citations": citations,
                                }
                            )
                        else:
                            st.error(
                                f"Error: {result.get('message', 'Unknown error occurred')}"
                            )

                    with st.expander("View source context"):
                        st.json(citations)


if __name__ == "__main__":
    main()
