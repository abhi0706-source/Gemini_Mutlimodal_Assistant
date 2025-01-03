import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json

from pydantic import ValidationError

from src.assistants.assistant_v1 import gemini_rag_assistant
from src.utils.knowledge_base import AgenticRAG


def main():
    rag = AgenticRAG(query_value=True)
    while True:
        query = input("Enter your query: ")
        results = rag.query(query_text=query, n_results=10)
        print("\nQuery Results:")
        print(json.dumps(results, indent=2))

        try:
            print("gemini start generating answer")
            response = gemini_rag_assistant.get_response_gemini(
                message=query, context_data=results
            )
            print("\nAssistant Response:")
            print(response)

        except ValidationError as e:
            print("Validation Error:", e)
            return {
                "source_id": "validation_error",
                "content": str(e),
            }

        except Exception as e:
            print("Internal Server Error:", e)
            return {
                "source_id": "internal_error",
                "content": "Internal Server Error",
            }


if __name__ == "__main__":
    main()
