import os
import sys

# Add the project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(project_root)

import json
import os
import re
import time
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import docx
import exceptiongroup
import google.generativeai as genai
import numpy as np
import pandas as pd
import PyPDF2
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from nanoid import generate
from pydantic import BaseModel, Field

from src.utils.vectorDB import VectorStore

load_dotenv()


class MetadataPDF(BaseModel):
    key_concepts: List[str] = Field(
        ..., description="Key concepts related to the topic"
    )
    page_number: int = Field(
        ...,
        alias="page-number",
        description="The page number where this content is located",
    )


class SegmentPDF(BaseModel):
    content: str = Field(..., description="The main text of the segment")
    metadata: MetadataPDF


class AnalyzedContentPDF(BaseModel):
    segments: List[SegmentPDF] = Field(
        ..., description="List of meaningful content segments"
    )


# for text data


class MetadataTxt(BaseModel):
    key_concepts: List[str] = Field(
        ..., description="Key concepts related to the topic"
    )


class SegmentTxt(BaseModel):
    content: str = Field(..., description="The main text of the segment")
    metadata: MetadataTxt


class AnalyzedContentTxt(BaseModel):
    segments: List[SegmentTxt] = Field(
        ..., description="List of meaningful content segments"
    )


class GeminiChunker:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)
        # self.model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")
        self.model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        # self.model = genai.GenerativeModel(model_name="gemini-1.5-pro")

    def check_file_ready(self, file):
        while file.state.name == "PROCESSING":
            print(".", end="")
            time.sleep(10)
            file = genai.get_file(file.name)

        if file.state.name == "FAILED":
            raise ValueError(f"File processing failed: {file.state.name}")

    def chunk_with_gemini(
        self, content: str, content_type: str
    ) -> List[Dict[str, Any]]:
        # cleaned_content = "".join(
        #     char for char in content if ord(char) >= 32 or char in "\n\r\t"
        # )

        # # Encode and decode to handle unsupported characters
        # safe_string = cleaned_content.encode("utf-8", errors="replace").decode("utf-8")
        # print(safe_string)

        if content_type == "pdf" or content_type == "docx":
            """Use Gemini to intelligently chunk content based on semantic understanding"""
            prompt = f"""
            Analyze the following {content_type} content first means read whole content first then after divide it into complete and meaningful segments (chunks). 
            Each chunk size has 512 token should:
            1. Be self-contained and end at logical boundaries (e.g., complete sentences or sections).
            2. Include all text that belongs to a single segment without truncation.
            3. Ensure the last chunk is fully complete and not cut off.

            Return the response strictly in the specified schema format:

                {{
                    "content": "segment text here",
                    "metadata": {{
                        "key_concepts": ["concept1", "concept2"],
                        "page-number": 64
                    }}
                }},
                // more segments...

            Content to analyze:
            {content}

            Keep the response as pure JSON without any additional text or explanation. Avoid splitting content mid-sentence or mid-thought.
            All chunks should be complete.
            """
            schema = AnalyzedContentPDF
        else:
            prompt = f"""
            Analyze the following {content_type} content first means read whole content first then after divide it into complete and meaningful segments (chunks). 
            Each chunk should:
            1. Be self-contained and end at logical boundaries (e.g., complete sentences or sections).
            2. Include all text that belongs to a single segment without truncation.
            3. Ensure the last chunk is fully complete and not cut off.

            Return the response strictly in the specified schema format:

                {{
                    "content": "segment text here",
                    "metadata": {{
                        "key_concepts": ["concept1", "concept2"],
                        "page-number": NA
                    }}
                }},
                // more segments...

            Content to analyze:
            {content}

            Keep the response as pure JSON without any additional text or explanation. Avoid splitting content mid-sentence or mid-thought.
            All chunks should be complete.
            """
            schema = AnalyzedContentTxt

        print(schema)

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                ),
            )
            # print(response.text)
            cleaned_text = "".join(
                char for char in response.text if ord(char) >= 32 or char in "\n\r\t"
            )
            with open("chunking_text.txt", "w", encoding="utf-8") as file_text:
                print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                file_text.write(cleaned_text)
                print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

            cleaned_text = cleaned_text.encode("utf-8", errors="replace").decode(
                "utf-8"
            )

            result = json.loads(cleaned_text)

            # print(result)

            print("pdf parsing")

            chunks = []

            for segment in result.get("segments", []):
                # print("################################")
                # print(segment.get("content", ""))
                # print("################################")
                temp_metadata = segment["metadata"]
                if content_type == "pdf":
                    chunk = {
                        "content": segment.get("content", ""),
                        "metadata": {
                            "topics": temp_metadata.get("key_concepts", []),
                            "page-number": temp_metadata.get("page-number", ""),
                            "type": "pdf",
                        },
                    }
                else:
                    chunk = {
                        "content": segment.get("content", ""),
                        "metadata": {
                            "topics": segment.get("key_concepts", []),
                            "page-number": segment.get("page-number", ""),
                            "type": "text",
                        },
                    }
                chunks.append(chunk)

            # print()
            # print()
            # print("chunks:")
            # print(chunks)
            # print()
            # print()

            return chunks

        except Exception as e:
            print(f"Error in Gemini chunking: {e}")
            return [
                {
                    "content": content,
                    "metadata": {
                        "topics": "",
                        "page-number": "0",
                    },
                }
            ]

    def process_media_file(
        self, file_path: str, media_type: str
    ) -> List[Dict[str, Any]]:
        """Process video or audio file using Gemini's media understanding"""
        try:
            print("here-0!!!")
            media_file = genai.upload_file(path=file_path)
            self.check_file_ready(media_file)
            print("here-1!!!")

            if media_type == "video":
                schema = {
                    "type": "object",
                    "properties": {
                        "segments": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "timestamp": {"type": "string"},
                                    "description": {"type": "string"},
                                    "topics": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    },
                                },
                            },
                        }
                    },
                }

                prompt = "Describe this video in detail, breaking it into timestamped segments. Include key events and actions."
            else:  # audio
                schema = {
                    "type": "object",
                    "properties": {
                        "segments": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "timestamp": {"type": "string"},
                                    "transcription": {"type": "string"},
                                    "speaker": {"type": "string"},
                                    "topics": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    },
                                },
                            },
                        }
                    },
                }

                prompt = "Transcribe this audio, identifying speakers and key topics discussed."

            print("Here-2!!!")
            response = self.model.generate_content(
                [media_file, prompt],
                generation_config=genai.GenerationConfig(
                    response_schema=schema, response_mime_type="application/json"
                ),
            )
            print("Here-3!!!")

            # Convert Gemini's media response to our standard chunk format
            print(response.text)
            print("Here-4!!!")
            cleaned_text = "".join(
                char for char in response.text if ord(char) >= 32 or char in "\n\r\t"
            )
            result = json.loads(cleaned_text)
            # result = json.loads(response.text)
            chunks = []
            print("Here-5!!!")

            for segment in result.get("segments", []):
                if media_type == "video":
                    chunk = {
                        "content": segment.get("description", ""),
                        "metadata": {
                            "timestamp": segment.get("timestamp", ""),
                            "topics": segment.get("key_events", []),
                            "type": "video",
                        },
                    }
                else:
                    chunk = {
                        "content": segment.get("transcription", ""),
                        "metadata": {
                            "timestamp": segment.get("timestamp", ""),
                            "speaker": segment.get("speaker", ""),
                            "topics": segment.get("topics", []),
                            "type": "audio",
                        },
                    }
                chunks.append(chunk)
            print("Here-6!!!")

            return chunks

        except Exception as e:
            print(f"Error processing {media_type} file: {e}")
            return [
                {
                    "content": f"Error processing {media_type} file",
                    "metadata": {"type": media_type, "error": str(e)},
                }
            ]


class ContentProcessor:
    def __init__(self):
        self.gemini_chunker = GeminiChunker()

    def process_text(self, text: str, source_type: str) -> List[Dict[str, Any]]:
        """Process any text content using Gemini chunking"""
        chunks = self.gemini_chunker.chunk_with_gemini(text, source_type)
        for chunk in chunks:
            chunk["metadata"]["source_type"] = source_type
        return chunks

    def process_pdf(self, file_path: str) -> List[Dict[str, Any]]:
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            full_text = ""
            for page in pdf_reader.pages:
                full_text += page.extract_text() + " "
        return self.process_text(full_text, "pdf")

    def process_docx(self, file_path: str) -> List[Dict[str, Any]]:
        doc = docx.Document(file_path)
        full_text = " ".join([paragraph.text for paragraph in doc.paragraphs])
        return self.process_text(full_text, "docx")

    def process_csv(self, file_path: str) -> List[Dict[str, Any]]:
        df = pd.read_csv(file_path)
        # Convert DataFrame to a more readable format for Gemini
        text_content = df.to_string()
        return self.process_text(text_content, "csv")

    def process_webpage(self, url: str) -> List[Dict[str, Any]]:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        return self.process_text(text, "webpage")

    def process_video(self, file_path: str) -> List[Dict[str, Any]]:
        """Process video using Gemini's video understanding capabilities"""
        print("in process function of video")
        video_file = genai.upload_file(path=file_path)
        self.gemini_chunker.check_file_ready(video_file)

        chunks = self.gemini_chunker.process_media_file(
            file_path=file_path, media_type="video"
        )
        return chunks

    def process_audio(self, file_path: str) -> List[Dict[str, Any]]:
        """Process audio using Gemini's audio understanding capabilities"""
        print("in process function of audio")
        audio_file = genai.upload_file(path=file_path)
        self.gemini_chunker.check_file_ready(audio_file)

        chunks = self.gemini_chunker.process_media_file(
            file_path=file_path, media_type="audio"
        )
        return chunks


class AgenticRAG:
    def __init__(self, query_value=False, is_uploaded=False):
        self.processor = ContentProcessor()
        self.vector_store = VectorStore(query=query_value, is_uploaded=is_uploaded)
        if query_value == False and is_uploaded == True:
            self.json_file_path = "json_file_record.json"
        else:
            self.json_file_path = "utils/json_file_record.json"

    def process_file(self, file_path: str, file_type: Optional[str] = None):
        if file_type is None:
            file_type = self._detect_file_type(file_path)

        if os.path.exists(self.json_file_path):
            with open(self.json_file_path, "r") as json_file:
                json_data = json.load(json_file)
                for record in json_data:
                    if record["file_path"] == file_path:
                        return True  # File path exists
        try:
            chunks = []
            if file_type == "pdf":
                chunks = self.processor.process_pdf(file_path)
            elif file_type == "docx":
                chunks = self.processor.process_docx(file_path)
            elif file_type == "csv":
                chunks = self.processor.process_csv(file_path)
            elif file_type == "url":
                chunks = self.processor.process_webpage(file_path)
            elif file_type == "video":
                chunks = self.processor.process_video(file_path)
            elif file_type == "audio":
                chunks = self.processor.process_audio(file_path)
            elif file_type == "text":
                with open(file_path, "r") as file:
                    chunks = self.processor.process_text(file.read(), "text")

            if chunks:
                # Add source information to metadata
                print("in processfile fucntion file.")
                for chunk in chunks:
                    chunk["metadata"]["source"] = file_path

                print(chunks)

                # Add to Vector Database.
                self.vector_store.add_documents(chunks)
                print(f"Successfully processed {file_path} with {len(chunks)} chunks")

                return True
            return False

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    def _detect_file_type(self, file_path: str) -> str:
        if file_path.startswith("http"):
            return "url"

        extension = file_path.split(".")[-1].lower()
        type_mapping = {
            "pdf": "pdf",
            "docx": "docx",
            "doc": "docx",
            "csv": "csv",
            "txt": "text",
            "mp3": "audio",
            "wav": "audio",
            "mp4": "video",
            "mov": "video",
        }
        return type_mapping.get(extension, "unknown")

    def query(self, query_text: str, n_results: int = 5) -> Dict:
        return self.vector_store.query(query_text, n_results)


# Define a function to determine the file type based on the extension
def get_file_type(file_name: str) -> str:
    if file_name.endswith(".mp3"):
        return "audio"
    elif file_name.endswith(".mp4"):
        return "video"
    elif file_name.endswith(".csv"):
        return "csv"
    elif file_name.endswith(".pdf"):
        return "pdf"
    elif file_name.endswith(".docx"):
        return "docx"
    elif file_name.startswith("http"):
        return "url"
    else:
        return "unknown"


def main():
    # Initialize the RAG system
    rag = AgenticRAG(is_uploaded=True)

    # Automatically read the files in the 'data' directory
    data_directory = "../data"
    test_files = []

    # Loop through all files in the 'data' directory
    for filename in os.listdir(data_directory):
        file_path = os.path.join(data_directory, filename)
        if os.path.isfile(file_path):  # Check if it's a file
            file_type = get_file_type(filename)
            test_files.append((file_path, file_type))

    # Process each file
    for file_path, file_type in test_files:
        print(f"\nProcessing {file_path}...")
        time.sleep(5)
        rag.process_file(file_path, file_type)


if __name__ == "__main__":
    main()
