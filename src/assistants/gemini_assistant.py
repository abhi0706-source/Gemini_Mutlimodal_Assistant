# import json
# import os
# from dataclasses import dataclass
# from enum import Enum
# from typing import Any, Dict, List, Optional, Union

# import google.generativeai as genai
# from pydantic import BaseModel


# class Role(Enum):
#     USER = "user"
#     ASSISTANT = "assistant"
#     SYSTEM = "system"


# @dataclass
# class Message:
#     role: Role
#     content: str


# class GeminiAssistant:
#     def __init__(
#         self,
#         api_key: str,
#         model: str = "gemini-pro",
#         temperature: float = 0.7,
#         top_p: float = 0.95,
#         top_k: int = 40,
#         max_output_tokens: int = 2048,
#         system_prompt: Optional[str] = None,
#         output_model: Optional[type[BaseModel]] = None,
#     ):
#         genai.configure(api_key=api_key)

#         self.model = genai.GenerativeModel(
#             model_name=model,
#             system_instruction=system_prompt,
#             generation_config={
#                 "temperature": temperature,
#                 "top_p": top_p,
#                 "top_k": top_k,
#                 "max_output_tokens": max_output_tokens,
#                 "response_mime_type": "application/json",
#             },
#         )

#         self.system_prompt = system_prompt
#         self.output_model = output_model
#         self.conversation_history: List[Message] = []
#         if system_prompt:
#             self.conversation_history.append(
#                 Message(role=Role.SYSTEM, content=system_prompt)
#             )

#     def add_message(self, role: Union[Role, str], content: str) -> None:
#         if isinstance(role, str):
#             role = Role(role)
#         self.conversation_history.append(Message(role=role, content=content))

#     def _format_messages_for_gemini(self) -> List[Dict]:
#         """Convert internal message format to Gemini's expected format."""
#         formatted_history = []

#         for msg in self.conversation_history:
#             if msg.role == Role.USER:
#                 formatted_history.append(
#                     {"role": "user", "parts": [{"text": msg.content}]}
#                 )
#             elif msg.role == Role.ASSISTANT:
#                 formatted_history.append(
#                     {"role": "model", "parts": [{"text": msg.content}]}
#                 )
#             # System messages are handled differently

#         return formatted_history

#     async def get_response(
#         self,
#         message: str,
#         context_data: Optional[str] = None,
#     ) -> Union[str, BaseModel]:
#         """Get a response from the assistant for the given message."""
#         # Prepare the full message with system prompt if it exists
#         full_message = message
#         if self.system_prompt and not self.conversation_history:
#             full_message = (
#                 f"{self.system_prompt}\n\n{message}\n\nContext:\n{context_data}\n"
#             )
#         else:

#             full_message = f"{message}\n\nContext:\n{context_data}\n"

#         print("********************")
#         print(full_message)
#         print("********************")

#         # Add user message to history
#         self.add_message(Role.USER, full_message)

#         try:
#             # Create chat session with properly formatted history
#             chat = self.model.start_chat(history=self._format_messages_for_gemini())

#             # Generate response
#             response = await chat.send_message_async(full_message)
#             response_text = response.text

#             # Handle structured output if output_model is specified
#             if self.output_model:
#                 try:
#                     # Try to parse the response as JSON
#                     response_data = json.loads(response_text)
#                     # Validate with Pydantic model
#                     structured_response = self.output_model(**response_data)
#                     # Add the formatted response to history
#                     self.add_message(
#                         Role.ASSISTANT, json.dumps(response_data, indent=2)
#                     )
#                     return structured_response
#                 except (json.JSONDecodeError, ValueError) as e:
#                     # If parsing fails, try to fix the response format
#                     retry_prompt = (
#                         "Please format your previous response as a valid JSON object "
#                         "that matches the specified schema. Include all required fields."
#                     )
#                     response = await chat.send_message_async(retry_prompt)
#                     try:
#                         print(response.text)
#                         response_data = json.loads(response.text)
#                         structured_response = self.output_model(**response_data)
#                         self.add_message(
#                             Role.ASSISTANT, json.dumps(response_data, indent=2)
#                         )
#                         return structured_response
#                     except (json.JSONDecodeError, ValueError) as e:
#                         raise ValueError(
#                             f"Failed to generate properly formatted response: {str(e)}"
#                         )
#             else:
#                 # Handle regular string response
#                 self.add_message(Role.ASSISTANT, response_text)
#                 return response_text

#         except Exception as e:
#             raise Exception(f"Error generating response: {str(e)}")

#     def clear_history(self) -> None:
#         """Clear the conversation history."""
#         self.conversation_history = []
#         if self.system_prompt:
#             self.add_message(Role.SYSTEM, self.system_prompt)


# # Example usage
# async def main():
#     # Initialize assistant
#     assistant = GeminiAssistant(
#         api_key="your-api-key-here", system_prompt="You are a helpful AI assistant."
#     )

#     # Get response
#     response = await assistant.get_response("What is machine learning?")
#     print(response)

#     # Continue conversation
#     response = await assistant.get_response("Can you give me an example?")
#     print(response)


# if __name__ == "__main__":
#     import asyncio

#     asyncio.run(main())


# import json
# import os
# from dataclasses import dataclass
# from enum import Enum
# from typing import Any, Dict, List, Optional, Union

# import google.generativeai as genai
# from pydantic import BaseModel


# class Role(Enum):
#     USER = "user"
#     ASSISTANT = "assistant"
#     SYSTEM = "system"


# @dataclass
# class Message:
#     role: Role
#     content: str


# class GeminiAssistant:
#     def __init__(
#         self,
#         api_key: str,
#         model: str = "gemini-pro",
#         temperature: float = 0.7,
#         top_p: float = 0.95,
#         top_k: int = 40,
#         max_output_tokens: int = 2048,
#         system_prompt: Optional[str] = None,
#         output_model: Optional[type[BaseModel]] = None,
#     ):
#         genai.configure(api_key=api_key)

#         self.model = genai.GenerativeModel(
#             model_name=model,
#             system_instruction=system_prompt,
#             generation_config={
#                 "temperature": temperature,
#                 "top_p": top_p,
#                 "top_k": top_k,
#                 "max_output_tokens": max_output_tokens,
#                 "response_mime_type": "application/json",
#             },
#         )

#         self.system_prompt = system_prompt
#         self.output_model = output_model
#         self.conversation_history: List[Message] = []
#         if system_prompt:
#             self.conversation_history.append(
#                 Message(role=Role.SYSTEM, content=system_prompt)
#             )

#     def add_message(self, role: Union[Role, str], content: str) -> None:
#         if isinstance(role, str):
#             role = Role(role)
#         self.conversation_history.append(Message(role=role, content=content))

#     def _format_messages_for_gemini(self) -> List[Dict]:
#         """Convert internal message format to Gemini's expected format."""
#         formatted_history = []

#         for msg in self.conversation_history:
#             if msg.role == Role.USER:
#                 formatted_history.append(
#                     {"role": "user", "parts": [{"text": msg.content}]}
#                 )
#             elif msg.role == Role.ASSISTANT:
#                 formatted_history.append(
#                     {"role": "model", "parts": [{"text": msg.content}]}
#                 )
#             # System messages are handled differently

#         return formatted_history

#     async def get_response_gemini(
#         self,
#         message: str,
#         context_data: Optional[str] = None,
#     ) -> Union[str, BaseModel]:
#         """Get a response from the assistant for the given message."""
#         # Prepare the full message with system prompt if it exists
#         full_message = message
#         if self.system_prompt and not self.conversation_history:
#             full_message = (
#                 f"{self.system_prompt}\n\n{message}\n\nContext:\n{context_data}\n"
#             )
#         else:
#             full_message = f"{message}\n\nContext:\n{context_data}\n"

#         print("********************")
#         print(full_message)
#         print("********************")

#         # Add user message to history
#         self.add_message(Role.USER, full_message)

#         try:
#             # Create chat session with properly formatted history
#             chat = self.model.start_chat(history=self._format_messages_for_gemini())

#             # Generate response
#             response = await chat.send_message_async(full_message)
#             response_text = response.text

#             # Handle structured output if output_model is specified
#             if self.output_model:
#                 try:
#                     # Try to parse the response as JSON
#                     response_data = json.loads(response_text)

#                     # Ensure required fields are present
#                     if "source_id" not in response_data:
#                         response_data["source_id"] = "default_source_id"
#                     if "quote" not in response_data:
#                         response_data["quote"] = "default_quote"

#                     # Validate with Pydantic model
#                     structured_response = self.output_model(**response_data)
#                     # Add the formatted response to history
#                     self.add_message(
#                         Role.ASSISTANT, json.dumps(response_data, indent=2)
#                     )
#                     return structured_response
#                 except (json.JSONDecodeError, ValueError) as e:
#                     # If parsing fails, try to fix the response format
#                     retry_prompt = (
#                         "Please format your previous response as a valid JSON object "
#                         "that matches the specified schema. Include all required fields."
#                     )
#                     response = await chat.send_message_async(retry_prompt)
#                     try:
#                         print(response.text)
#                         response_data = json.loads(response.text)

#                         # Ensure required fields are present
#                         if "source_id" not in response_data:
#                             response_data["source_id"] = "default_source_id"
#                         if "quote" not in response_data:
#                             response_data["quote"] = "default_quote"

#                         structured_response = self.output_model(**response_data)
#                         self.add_message(
#                             Role.ASSISTANT, json.dumps(response_data, indent=2)
#                         )
#                         return structured_response
#                     except (json.JSONDecodeError, ValueError) as e:
#                         raise ValueError(
#                             f"Failed to generate properly formatted response: {str(e)}"
#                         )
#             else:
#                 # Handle regular string response
#                 self.add_message(Role.ASSISTANT, response_text)
#                 return response_text

#         except Exception as e:
#             raise Exception(f"Error generating response: {str(e)}")

#     def clear_history(self) -> None:
#         """Clear the conversation history."""
#         self.conversation_history = []
#         if self.system_prompt:
#             self.add_message(Role.SYSTEM, self.system_prompt)


import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union

import google.generativeai as genai
from pydantic import BaseModel


class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class Message:
    role: Role
    content: str


class GeminiAssistant:
    def __init__(
        self,
        api_key: str,
        model: str = "gemini-pro",
        temperature: float = 0.7,
        top_p: float = 0.95,
        top_k: int = 40,
        max_output_tokens: int = 2048,
        system_prompt: Optional[str] = None,
        output_model: Optional[type[BaseModel]] = None,
    ):
        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel(
            model_name=model,
            system_instruction=system_prompt,
            generation_config={
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "max_output_tokens": max_output_tokens,
                "response_mime_type": "application/json",
            },
        )

        self.system_prompt = system_prompt
        self.output_model = output_model
        self.conversation_history: List[Message] = []
        if system_prompt:
            self.conversation_history.append(
                Message(role=Role.SYSTEM, content=system_prompt)
            )

    def add_message(self, role: Union[Role, str], content: str) -> None:
        if isinstance(role, str):
            role = Role(role)
        self.conversation_history.append(Message(role=role, content=content))

    def _format_messages_for_gemini(self) -> List[Dict]:
        """Convert internal message format to Gemini's expected format."""
        formatted_history = []

        for msg in self.conversation_history:
            if msg.role == Role.USER:
                formatted_history.append(
                    {"role": "user", "parts": [{"text": msg.content}]}
                )
            elif msg.role == Role.ASSISTANT:
                formatted_history.append(
                    {"role": "model", "parts": [{"text": msg.content}]}
                )

        return formatted_history

    def get_response_gemini(
        self,
        message: str,
        context_data: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get a response from the assistant for the given message."""
        full_message = message
        if self.system_prompt and not self.conversation_history:
            full_message = (
                f"{self.system_prompt}\n\n{message}\n\nContext:\n{context_data}\n"
            )
        else:
            full_message = f"{message}\n\nContext:\n{context_data}\n"

        # Add user message to history
        self.add_message(Role.USER, full_message)

        try:
            # Create chat session with properly formatted history
            chat = self.model.start_chat(history=self._format_messages_for_gemini())

            # Generate response
            response = chat.send_message(full_message)
            response_text = response.text

            # Parse response as JSON
            try:
                response_data = json.loads(response_text)

                # Ensure required fields are present
                if "source_id" not in response_data:
                    response_data["source_id"] = "default_source_id"
                if "quote" not in response_data:
                    response_data["quote"] = "default_quote"

                # Validate with Pydantic model if specified
                if self.output_model:
                    structured_response = self.output_model(**response_data)
                    self.add_message(
                        Role.ASSISTANT, json.dumps(response_data, indent=2)
                    )
                    return structured_response.dict()

                # Add response to history and return as dict
                self.add_message(Role.ASSISTANT, response_text)
                return response_data

            except (json.JSONDecodeError, ValueError) as e:
                raise ValueError(
                    f"Failed to parse response as JSON: {str(e)}. Response: {response_text}"
                )

        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []
        if self.system_prompt:
            self.add_message(Role.SYSTEM, self.system_prompt)
