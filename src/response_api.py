# import os
# import sys

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import json

# from pydantic import ValidationError
# from src.assistants.assistant_v1 import gemini_rag_assistant
# from src.utils.knowledge_base import AgenticRAG


# async def get_response(query=True, is_uploaded=False):
#     rag = AgenticRAG(query_value=query, is_uploaded=is_uploaded)

#     # query = input("Enter your query: ")
#     context = rag.query(query_text=query, n_results=10)
#     print("\nQuery Results:")
#     print(json.dumps(context, indent=2))

#     try:
#         response = await gemini_rag_assistant.get_response(
#             message=query, context_data=context
#         )
#         print("\nAssistant Response:")
#         print(response)

#         return {"response": response, "context": context}

#     except ValidationError as e:
#         print("Validation Error:", e)
#         return {
#             "source_id": "validation_error",
#             "content": str(e),
#         }

#     except Exception as e:
#         print("Internal Server Error:", e)
#         return {
#             "source_id": "internal_error",
#             "content": "Internal Server Error",
#         }


# async def main():
#     rag = AgenticRAG(query_value=True)
#     # while True:
#     query = input("Enter your query: ")
#     results = rag.query(query_text=query, n_results=10)
#     print("\nQuery Results:")
#     print(json.dumps(results, indent=2))

#     try:
#         print("gemini start generating answer")
#         response = await gemini_rag_assistant.get_response(
#             message=query, context_data=results
#         )
#         print("\nAssistant Response:")
#         print(response)

#     except ValidationError as e:
#         print("Validation Error:", e)
#         return {
#             "source_id": "validation_error",
#             "content": str(e),
#         }

#     except Exception as e:
#         print("Internal Server Error:", e)
#         return {
#             "source_id": "internal_error",
#             "content": "Internal Server Error",
#         }


# if __name__ == "__main__":
#     import asyncio

#     asyncio.run(main())


import json
import os
import traceback

import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError

from agents_rag.crew import get_crew_response
from assistants.assistant_v1 import gemini_rag_assistant
from utils.knowledge_base import AgenticRAG
from utils.vectorDB import VectorStore

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize FastAPI app
app = FastAPI(title="Gemini RAG Assistant API", version="1.0.0")


# Pydantic model for request body
class QueryRequest(BaseModel):
    query: str
    is_uploaded: bool = False
    url: str


# Pydantic model for response
class QueryResponse(BaseModel):
    response: str
    context: dict


def llm_answer(query=""):
    try:
        # Initialize Gemini RAG assistant
        model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")

        print("query", query)

        response = model.generate_content(query)
        print(response.text)

        return {"response": response.text, "status": "success"}

    except Exception as e:
        print(f"Error in Gemini chunking: {e}")
        return [
            {
                "response": "",
                "status": "fail",
            }
        ]


@app.post("/get-response")
def get_response(request: QueryRequest):
    """
    Endpoint to process a query and get a response from the assistant.
    """
    try:
        # Initialize AgenticRAG and fetch context
        rag = AgenticRAG(query_value=request.query, is_uploaded=request.is_uploaded)
        context = rag.query(query_text=request.query, n_results=15)

        print("Generate answer form gemini")
        # Fetch response from gemini assistant
        # response = gemini_rag_assistant.get_response_gemini(
        #     message=request.query, context_data=context
        # )

        response = get_crew_response(
            query=request.query, context=context, url=request.url
        )

        print(response)

        cleaned_text = "".join(
            char for char in response if ord(char) >= 32 or char in "\n\r\t"
        )

        result = dict(json.loads(cleaned_text))
        # print(result)
        result_answer = {
            "response": "",
            "context": "",
            "citations": "",
        }
        print("***************************")
        if "Answer" in result.keys():
            result_answer = {
                "response": result["Answer"],
                "context": result["context"],
                "citations": result["citations"],
            }
        elif "answer" in result.keys():

            result_answer = {
                "response": result["answer"],
                "context": result["context"],
                "citations": result["citations"],
            }
        print("***************************")
        print(result_answer)

        return result_answer

    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Validation Error: {e}")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Value Error: {e}")

    except Exception as e:
        traceback.print_exc()  # Log the full traceback
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.post("/llm-response")
def get_response_llm(request: dict):
    """
    Endpoint to process a query and get a response from the assistant.
    """
    try:
        # Initialize AgenticRAG and fetch context

        print("Generate answer form gemini")
        # Fetch response from gemini assistant

        result = llm_answer(query=request["query"])

        result = {
            "response": result["response"],
        }
        # print(result)

        return result

    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Validation Error: {e}")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Value Error: {e}")

    except Exception as e:
        traceback.print_exc()  # Log the full traceback
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.get("/health")
def health_check():
    """
    Endpoint for health check.
    """
    return {"status": "ok"}


@app.post("/delete-file")
async def process_upload_data(request: dict):
    """
    Endpoint to retrieve do emedding of new file and store the result in Vector database.
    """
    try:
        db = VectorStore()

        print("deletion started.")
        db.delete_documents_by_filename(request["file_path"])
        print("deletion end.")

        return {"response": 200}

    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Validation Error: {e}")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Value Error: {e}")

    except Exception as e:
        traceback.print_exc()  # Log the full traceback
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.post("/process-file")
async def process_upload_data(request: dict):
    """
    Endpoint to retrieve do emedding of new file and store the result in Vector database.
    """
    try:
        # Initialize AgenticRAG and fetch context
        rag = AgenticRAG(is_uploaded=False)

        print("process started.")
        rag.process_file(request["file_path"])
        print("process end.")

        # rag = AgenticRAG(query_value=request.query)
        # context = rag.query(query_text=request.query, n_results=10)

        # # Fetch response from gemini assistant
        # response = await gemini_rag_assistant.get_response(
        #     message=request.query, context_data=context
        # )

        # # Ensure response is in correct format
        # if not isinstance(response, str):
        #     raise ValueError("Unexpected response format from gemini_rag_assistant.")

        return {"response": 200}

    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Validation Error: {e}")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Value Error: {e}")

    except Exception as e:
        traceback.print_exc()  # Log the full traceback
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
