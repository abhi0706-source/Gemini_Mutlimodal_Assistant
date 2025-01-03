# import os
# from typing import List

# import google.generativeai as genai
# from dotenv import load_dotenv
# from langchain.prompts import PromptTemplate
# from langchain.schema import StrOutputParser
# from pydantic import BaseModel, Field

# from .gemini_assistant import GeminiAssistant

# load_dotenv()

# api_key = os.getenv("GEMINI_API_KEY")
# model_name = "gemini-2.0-flash-exp"


# class GenerativeAnswer(BaseModel):
#     answer: str = Field(
#         ...,
#         description="""The answer to the user question, which is based only on the given sources.\n
#         example: Artificial neural networks were inspired by information processing and distributed communication nodes in biological systems. ANNs have various differences from biological brains. Specifically, artificial neural networks tend to be static and symbolic, while the biological brain of most living organisms is dynamic (plastic) and analog (vec-001). However, ANNs have demonstrated significant capabilities in tasks such as pattern recognition, classification, and prediction, making them valuable tools in various fields (vec-002). Despite their effectiveness in certain applications, ANNs still lack the complexity and adaptability of biological brains, leading some researchers to view them as low-quality models for brain function (vec-003). Furthermore, advancements in neuroscience continue to provide insights into the workings of the brain, which may further differentiate artificial neural networks from their biological counterparts (vec-004). However, ANNs remain a powerful computational tool, offering practical solutions to a wide range of problems, albeit with inherent limitations compared to biological systems (vec-005) and so on.....
#         """,
#     )
#     source_id: List[str] = Field(
#         ...,
#         description="The ID of a SPECIFIC source which justifies the answer.",
#     )
#     quote: List[str] = Field(
#         ...,
#         description="The VERBATIM quote from the specified source that justifies the answer.",
#     )
#     related_questions: List[str] = Field(
#         ...,
#         description="Related questions based on the user question and generated answer.",
#     )

#     # [INST]<<SYS>>You are an Intelligent Assistant for question-answering tasks.
#     # Your knowledge base consists of documents related to Convene and its resources.
#     # Convene is a community of Christian business leaders who gather monthly in advisory teams worldwide to share insights, face challenges, and grow in faith through executive learning. Members can join or lead a Convene Team, participate in One2One™ Coaching, and access exclusive events. The organization, founded in 1996 by Brian Thatcher and others from Saddleback Church, aims to help CEOs integrate faith with business to build profitable, faith-based enterprises. Services include peer advisory, executive coaching, and business consulting, focusing on enhancing business and leadership skills while maintaining a faith foundation. Convene emphasizes balancing business success with spiritual growth and family leadership.

#     # Your [Task] is to answer questions accurately and concisely based on the context provided. You will strictly discuss topics within the scope of the context provided and Convene's activities, history, services, and community impacts as outlined.
#     # Identify if the User question aligns with the context or Convene's interests. If the information requested is outside of the context or Convene's provided data or knowledge base, You should politely decline the request and tell the user to ask related questions.
#     # Only provide answers based on the information available in your context and the above topics.

#     # Use the following steps and pieces of retrieved context to answer the question. The answer should be detailed and concise.


# prompt = """
#     You are a friendly and helpful assistant.
#     Ensure your answers are complete, unless the user requests a more concise approach.
#     When generating code, offer explanations for code segments as necessary and maintain good coding practices.
#     When presented with inquiries seeking information, provide answers that reflect a deep understanding of the field, guaranteeing their correctness.
#     For any non-english queries, respond in the same language as the prompt unless otherwise specified by the user.
#     For prompts involving reasoning, provide a clear explanation of each step in the reasoning process before presenting the final answer.

#     [Task]
#     Your task is to answer questions accurately and concisely based on the context provided. You will strictly discuss topics within the scope of the provided context, including its activities, history, services, and impacts.
#     Assess whether the user’s question aligns with the context or the specified areas of interest.
#     If the information requested falls outside the provided context or scope, politely decline the request and advise the user to ask relevant questions within the given context.
#     Only provide answers based on the information available in the given context and the specified areas of interest.

#     The answer should look like:
#     Example: Artificial neural networks were inspired by information processing and distributed communication nodes in biological systems. ANNs have various differences from biological brains. Specifically, artificial neural networks tend to be static and symbolic, while the biological brain of most living organisms is dynamic (plastic) and analog (vec-001). However, ANNs have demonstrated significant capabilities in tasks such as pattern recognition, classification, and prediction, making them valuable tools in various fields (vec-002). Despite their effectiveness in certain applications, ANNs still lack the complexity and adaptability of biological brains, leading some researchers to view them as low-quality models for brain function (vec-003). Furthermore, advancements in neuroscience continue to provide insights into the workings of the brain, which may further differentiate artificial neural networks from their biological counterparts (vec-004). However, ANNs remain a powerful computational tool, offering practical solutions to a wide range of problems, albeit with inherent limitations compared to biological systems (vec-005) and so on.....
#     means your answer must contains source_id in given format.
#     Output should follow the pattern defined in schema and the output should be in json format only so that it can be directly used with json.loads()
#     <</SYS>>
#     steps:
#     1. use the provided data.
#     2. Check if the question is related to Convene or related to the context provided. If the question is not related, ask them politely to ask related questions. Do not follow further steps but use the wrong_question_schema to output the answer.
#     3. use one source and extract the sentences from it that justify the answer all the source sentences are in must be unique.
#     4. use the sentences to generate the answer and append its source_id to the answer with prefix "vec-". You must append its source_id only if it exists. Do not hallucinate or add from your imagination. Only add source_id which you get from the context. This is a strict requirement.
#     5. use other source and extract the sentences from it that justify the answer. NOTE: use atleast 3 sources to generate the answer.
#     6. If the user has asked question related to the context or Convene, use the whole answer and user's question to generate 3 related questions. If the question is outside the context, do not generate related questions.

#     NOTE: Make sure no out of bounds questions or questions that are not in the context or knowledge base are answered. This is mandatory that no out of context questions are answered."""

# gemini_rag_assistant = GeminiAssistant(
#     model=model_name,
#     api_key=api_key,
#     system_prompt=prompt,
#     output_model=GenerativeAnswer,
# )


# import os
# from typing import List

# import google.generativeai as genai
# from dotenv import load_dotenv
# from langchain.prompts import PromptTemplate
# from langchain.schema import StrOutputParser
# from pydantic import BaseModel, Field

# from .gemini_assistant import GeminiAssistant

# # Load environment variables
# load_dotenv()

# # Load the API key from the environment
# api_key = os.getenv("GEMINI_API_KEY")
# model_name = "gemini-2.0-flash-exp"


# # Define the output model schema using Pydantic
# class GenerativeAnswer(BaseModel):
#     answer: str = Field(
#         ...,
#         description="""The answer to the user question, which is based only on the given sources.
#         Example:
#         Artificial neural networks were inspired by information processing and distributed communication nodes in biological systems.
#         ANNs have various differences from biological brains. Specifically, artificial neural networks tend to be static and symbolic,
#         while the biological brain of most living organisms is dynamic (plastic) and analog (vec-001). However, ANNs have demonstrated
#         significant capabilities in tasks such as pattern recognition, classification, and prediction, making them valuable tools in various fields
#         (vec-002). Despite their effectiveness in certain applications, ANNs still lack the complexity and adaptability of biological brains,
#         leading some researchers to view them as low-quality models for brain function (vec-003). Furthermore, advancements in neuroscience
#         continue to provide insights into the workings of the brain, which may further differentiate artificial neural networks from their biological counterparts
#         (vec-004). However, ANNs remain a powerful computational tool, offering practical solutions to a wide range of problems, albeit with inherent limitations
#         compared to biological systems (vec-005).""",
#     )
#     source_id: List[str] = Field(
#         ...,
#         description="The ID of a SPECIFIC source which justifies the answer.",
#     )
#     quote: List[str] = Field(
#         ...,
#         description="The VERBATIM quote from the specified source that justifies the answer.",
#     )
#     related_questions: List[str] = Field(
#         ...,
#         description="Related questions based on the user question and generated answer.",
#     )


# # Define the system prompt
# prompt = """
#     You are a friendly and helpful assistant.
#     Ensure your answers are complete, unless the user requests a more concise approach.
#     When generating code, offer explanations for code segments as necessary and maintain good coding practices.
#     When presented with inquiries seeking information, provide answers that reflect a deep understanding of the field, guaranteeing their correctness.
#     For any non-English queries, respond in the same language as the prompt unless otherwise specified by the user.
#     For prompts involving reasoning, provide a clear explanation of each step in the reasoning process before presenting the final answer.

#     [Task]
#     Your task is to answer questions accurately and concisely based on the context provided. You will strictly discuss topics within the scope of the provided context, including its activities, history, services, and impacts.
#     Assess whether the user’s question aligns with the context or the specified areas of interest.
#     If the information requested falls outside the provided context or scope, politely decline the request and advise the user to ask relevant questions within the given context.
#     Only provide answers based on the information available in the given context and the specified areas of interest.

#     The answer should look like:
#     Example: Artificial neural networks were inspired by information processing and distributed communication nodes in biological systems.
#     ANNs have various differences from biological brains. Specifically, artificial neural networks tend to be static and symbolic,
#     while the biological brain of most living organisms is dynamic (plastic) and analog (vec-001). However, ANNs have demonstrated
#     significant capabilities in tasks such as pattern recognition, classification, and prediction, making them valuable tools in various fields
#     (vec-002). Despite their effectiveness in certain applications, ANNs still lack the complexity and adaptability of biological brains,
#     leading some researchers to view them as low-quality models for brain function (vec-003). Furthermore, advancements in neuroscience
#     continue to provide insights into the workings of the brain, which may further differentiate artificial neural networks from their biological counterparts
#     (vec-004). However, ANNs remain a powerful computational tool, offering practical solutions to a wide range of problems, albeit with inherent limitations
#     compared to biological systems (vec-005).
#     Make sure your answer contains source_id in the given format.

#     Output should follow the pattern defined in the schema, and the output should be in JSON format only, so that it can be directly used with `json.loads()`.

#     Steps:
#     1. Use the provided data.
#     2. Check if the question is related to the context or related to the provided scope. If the question is not related, politely ask the user to ask relevant questions. Do not proceed with other steps and use the wrong_question_schema to output the answer.
#     3. Use one source and extract the sentences from it that justify the answer. All source sentences must be unique.
#     4. Use the sentences to generate the answer and append its source_id to the answer with prefix "vec-". You must append its source_id only if it exists. Do not hallucinate or add from your imagination. Only add source_id which you get from the context. This is a strict requirement.
#     5. Use other sources and extract the sentences from them that justify the answer. NOTE: Use at least 3 sources to generate the answer.
#     6. If the user has asked a question related to the context or scope, use the entire answer and the user's question to generate 3 related questions. If the question is outside the context, do not generate related questions.

#     NOTE: Ensure that no out-of-bounds questions or questions outside the context are answered. It is mandatory that no out-of-context questions are addressed.
# """

# # Instantiate the Gemini RAG assistant
# gemini_rag_assistant = GeminiAssistant(
#     model=model_name,
#     api_key=api_key,
#     system_prompt=prompt,
#     output_model=GenerativeAnswer,
# )

import os
from typing import List

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from .gemini_assistant import GeminiAssistant

# Load environment variables
load_dotenv()

# Load the API key from the environment
api_key = os.getenv("GEMINI_API_KEY")
model_name = "gemini-2.0-flash-exp"


# Define the output model schema using Pydantic
class GenerativeAnswer(BaseModel):
    answer: str = Field(
        ...,
        description="""The answer to the user question, which is based only on the given sources.
        Example:
        Artificial neural networks were inspired by information processing and distributed communication nodes in biological systems. 
        ANNs have various differences from biological brains. Specifically, artificial neural networks tend to be static and symbolic, 
        while the biological brain of most living organisms is dynamic (plastic) and analog (vec-001). However, ANNs have demonstrated 
        significant capabilities in tasks such as pattern recognition, classification, and prediction, making them valuable tools in various fields 
        (vec-002). Despite their effectiveness in certain applications, ANNs still lack the complexity and adaptability of biological brains, 
        leading some researchers to view them as low-quality models for brain function (vec-003). Furthermore, advancements in neuroscience 
        continue to provide insights into the workings of the brain, which may further differentiate artificial neural networks from their biological counterparts 
        (vec-004). However, ANNs remain a powerful computational tool, offering practical solutions to a wide range of problems, albeit with inherent limitations 
        compared to biological systems (vec-005).""",
    )
    related_questions: List[str] = Field(
        ...,
        description="Related questions based on the user question and generated answer.",
    )


# Define the system prompt using Langchain's PromptTemplate
prompt_template = """
    You are a friendly and helpful assistant.
    Ensure your answers are complete, unless the user requests a more concise approach.
    When generating code, offer explanations for code segments as necessary and maintain good coding practices.
    When presented with inquiries seeking information, provide answers that reflect a deep understanding of the field, guaranteeing their correctness.
    For any non-English queries, respond in the same language as the prompt unless otherwise specified by the user.
    For prompts involving reasoning, provide a clear explanation of each step in the reasoning process before presenting the final answer.

    [Task]
    Your task is to answer questions accurately and concisely based on the context provided. You will strictly discuss topics within the scope of the provided context, including its activities, history, services, and impacts.
    Assess whether the user’s question aligns with the context or the specified areas of interest.
    If the information requested falls outside the provided context or scope, politely decline the request and advise the user to ask relevant questions within the given context.
    Only provide answers based on the information available in the given context and the specified areas of interest.

    The answer should look like:
    Example: Artificial neural networks were inspired by information processing and distributed communication nodes in biological systems. 
    ANNs have various differences from biological brains. Specifically, artificial neural networks tend to be static and symbolic, 
    while the biological brain of most living organisms is dynamic (plastic) and analog (vec-001). However, ANNs have demonstrated 
    significant capabilities in tasks such as pattern recognition, classification, and prediction, making them valuable tools in various fields 
    (vec-002). Despite their effectiveness in certain applications, ANNs still lack the complexity and adaptability of biological brains, 
    leading some researchers to view them as low-quality models for brain function (vec-003). Furthermore, advancements in neuroscience 
    continue to provide insights into the workings of the brain, which may further differentiate artificial neural networks from their biological counterparts 
    (vec-004). However, ANNs remain a powerful computational tool, offering practical solutions to a wide range of problems, albeit with inherent limitations 
    compared to biological systems (vec-005).

    The final output should be structured like this:
    1. The complete answer to the user question.
    2. The source IDs appended to the answer, e.g., (vec-001, vec-002, vec-003).
    3. Related questions that might arise from the user's question.

    Output should be in the following format:
    {
      "answer": "<generated_answer_with_sources>",
      "related_questions": [<related_question_1>, <related_question_2>, <related_question_3>]
    }
"""


# Instantiate the Gemini RAG assistant with the prompt template and output parser
gemini_rag_assistant = GeminiAssistant(
    model=model_name,
    api_key=api_key,
    system_prompt=prompt_template,
    output_model=GenerativeAnswer,
)
