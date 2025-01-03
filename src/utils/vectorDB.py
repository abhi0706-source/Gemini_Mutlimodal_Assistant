import json
import os
import sys
from typing import Any, Dict, List

# Add the project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

import chromadb
import numpy as np
import torch
from nanoid import generate
from transformers import AutoModel, AutoTokenizer


def append_to_json(new_entries, filename="json_file_record.json"):
    """
    Append new entries to an existing JSON array file, or create a new one if it doesn't exist.

    Args:
        new_entries (list): List of dictionaries to append
        filename (str): Name of the JSON file
    """
    try:
        # Read existing data if file exists
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            with open(filename, "r") as f:
                data = json.load(f)
            if not isinstance(data, list):
                data = []
        else:
            data = []

        # # Append new entries
        # data.extend(new_entries)
        # print(data)

        # Write back the updated data
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    except json.JSONDecodeError:
        # Handle case where file exists but is not valid JSON
        data = new_entries
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)


class BERTEmbedder:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.model = AutoModel.from_pretrained("bert-base-uncased")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def get_embeddings(self, texts: List[str]) -> np.ndarray:
        embeddings = []
        self.model.eval()
        with torch.no_grad():
            for text in texts:
                inputs = self.tokenizer(
                    text,
                    padding=True,
                    truncation=True,
                    max_length=512,
                    return_tensors="pt",
                )
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
                outputs = self.model(**inputs)
                embeddings.append(outputs.last_hidden_state.mean(dim=1).cpu().numpy())
        return np.vstack(embeddings)


class VectorStore:
    def __init__(
        self, persist_directory: str = "../chroma_rag", query=False, is_uploaded=False
    ):
        try:
            if query == False and is_uploaded == True:
                print("Embbeding store mode.")
                print(f"Initializing ChromaDB with directory: {persist_directory}")
                self.client = chromadb.PersistentClient(path=persist_directory)
                print("ChromaDB client created successfully")

                self.collection = self.client.get_or_create_collection(
                    name="documents",
                    metadata={"hnsw:space": "cosine"},
                    embedding_function=None,  # We're using our own embeddings
                )
                print(f"Collection 'documents' ready")

                self.embedder = BERTEmbedder()
                print("BERT embedder initialized")

                # Check if collection has documents
                content = self.collection.get()
                print(f"Collection contains {len(content['documents'])} documents")
                self.json_file_path = "json_file_record.json"

            else:
                print("query mode")
                persist_directory = "chroma_rag"
                print(f"Initializing ChromaDB with directory: {persist_directory}")
                self.client = chromadb.PersistentClient(path=persist_directory)
                print("ChromaDB client created successfully")

                self.collection = self.client.get_or_create_collection(
                    name="documents",
                    metadata={"hnsw:space": "cosine"},
                    embedding_function=None,  # We're using our own embeddings
                )
                print(f"Collection 'documents' ready")

                self.embedder = BERTEmbedder()
                print("BERT embedder initialized")

                # Check if collection has documents
                content = self.collection.get()
                print(f"Collection contains {len(content['documents'])} documents")
                self.json_file_path = "utils/json_file_record.json"

        except Exception as e:
            print(f"Error initializing VectorStore: {e}")
            raise

    def is_collection_empty(self) -> bool:
        try:
            content = self.collection.get()
            return len(content["documents"]) == 0
        except Exception as e:
            print(f"Error checking collection: {e}")
            return True

    def add_documents(self, chunks: List[Dict[str, Any]]):
        try:
            texts = [chunk["content"] for chunk in chunks]
            metadatas = [chunk["metadata"] for chunk in chunks]

            print(f"Generating embeddings for {len(texts)} documents...")
            print(texts)
            embeddings = self.embedder.get_embeddings(texts)

            id_val = str(generate(size=8))
            print(f"Generated ID: {id_val}")

            if os.path.exists(self.json_file_path):

                with open(self.json_file_path, "r") as f:
                    data = json.load(f)
                    for chunk in chunks:
                        temp = {"id": id_val, "file_path": chunk["metadata"]["source"]}

                        break
                    # Append the new entry
                    data.append(temp)

                # Write the updated JSON data back to the file
                with open(self.json_file_path, "w") as file:
                    json.dump(data, file, indent=4)
            else:
                # Usage in your code would be:
                with open(self.json_file_path, "w") as f:
                    temp = []
                    for chunk in chunks:
                        temp.append(
                            {"id": id_val, "file_path": chunk["metadata"]["source"]}
                        )
                        break
                # Write the updated JSON data back to the file
                with open(self.json_file_path, "w") as file:
                    json.dump(temp, file, indent=4)

            print("*************")
            count = 0
            ids = []
            # Clean metadata
            for metadata in metadatas:
                metadata["topics"] = str(metadata["topics"])
                ids.append(f"{id_val}{count}")
                count += 1
            print(metadatas)
            print("------------------------")
            print(len(metadatas))

            print(f"Adding {len(texts)} documents to collection...")
            self.collection.add(
                embeddings=embeddings.tolist(),
                documents=texts,
                metadatas=metadatas,
                ids=ids,
            )

            # Verify addition
            collection_content = self.collection.get()
            print(
                f"Collection now contains {len(collection_content['documents'])} documents"
            )

            return True
        except Exception as e:
            print(f"Error adding documents: {e}")
            return False

    def query(self, query_text: str, n_results: int = 3) -> Dict:
        try:

            print(f"Generating embedding for query: {query_text}")
            query_embedding = self.embedder.get_embeddings([query_text])

            print("Checking collection content:")
            collection_content = self.collection.get()
            print(
                f"Number of documents in collection: {len(collection_content['documents'])}"
            )

            print("Executing query...")
            query_vector = query_embedding.tolist()
            results = self.collection.query(
                n_results=min(n_results, len(collection_content["documents"])),
                query_embeddings=query_vector,
            )

            # query_texts=[query_text],

            print(f"Query results: {json.dumps(results, indent=2)}")
            return results
        except Exception as e:
            print(f"Error during query: {e}")
            return {"error": str(e)}

    def delete_documents_by_filename(self, file_substring: str):
        """
        Delete documents from the collection and JSON file by matching a substring in the file path.

        Args:
            file_substring (str): Substring to match in the file paths.
            json_file (str): Path to the JSON file containing document metadata.
        """
        try:
            # Load JSON data
            print(file_substring)
            json_file = self.json_file_path
            if not os.path.exists(json_file):
                print(f"JSON file {json_file} does not exist.")
                return

            with open(json_file, "r") as f:
                data = json.load(f)

            # Find matching records
            matching_records = [
                record for record in data if file_substring in record["file_path"]
            ]
            if not matching_records:
                print(f"No records found matching substring: {file_substring}")
                return

            # print("record", record)

            # Get IDs of matching records
            matching_ids = [record["id"] for record in matching_records]
            print("maching_ids", matching_ids[0])

            # Remove matching records from JSON file
            updated_data = [
                record for record in data if record["id"] not in matching_ids
            ]

            print("updated data", updated_data)

            with open(json_file, "w") as f:
                json.dump(updated_data, f, indent=4)

            print(f"Deleted {len(matching_records)} records from JSON file.")
            # Retrieve all IDs in the collection
            all_ids = self.collection.get()["ids"]

            # Filter IDs that contain the substring "LDtz9CG5"
            ids_to_delete = [id_ for id_ in all_ids if matching_ids[0] in id_]

            # Delete those IDs from the collection
            if ids_to_delete:
                self.collection.delete(ids=ids_to_delete)
                print(
                    f"Deleted {len(ids_to_delete)} records with IDs containing 'LDtz9CG5'."
                )
            else:
                print("No matching IDs found.")
        except Exception as e:
            print(f"Error deleting documents: {e}")
