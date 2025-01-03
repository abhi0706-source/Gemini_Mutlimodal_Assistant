from crewai import Task

from agents_rag.agents import news_researcher, news_writer, rag_agent, writer_rag
from agents_rag.tools import tool

# Research task
research_task = Task(
    description=(
        "Identify the next big trend in {topic}."
        "Focus on identifying pros and cons and the overall narrative."
        "Your final report should clearly articulate the key points,"
        "its market opportunities, and potential risks."
    ),
    expected_output="A comprehensive 3 paragraphs long report on the latest AI trends.",
    tools=[tool],
    agent=news_researcher,
)

# Writing task with language model configuration
write_task = Task(
    description=(
        "Compose an insightful article on {topic}."
        "Focus on the latest trends and how it's impacting the industry."
        "This article should be easy to understand, engaging, and positive."
    ),
    expected_output="A 4 paragraph article on {topic} advancements formatted as markdown.",
    tools=[tool],
    agent=news_writer,
    async_execution=False,
    # output_file="new-blog-post.md",  # Example of output customization
)

write_rag_task = Task(
    description=(
        "Answer the Give query: {query} like RAG application from given url: {url} only. if user manention url then use only that url to answer the query otherwise you can do web-search to answer the qurey. "
        "Focus on the latest trends."
        "The answer should be easy to understand, engaging, and positive."
        "Also Show source of content That use to generate generate answer."
        "All source are also show in citation and each citation have number and in end there is map of citation number and source."
    ),
    expected_output="A Give normal length answer if user asked something specific like small or big or more this some type of word then give answer according to that length on {query} advancements formatted as only one JSON format. in which it has two field first is Answer in which generated answer is written and second field is context in which the context value that are used to for generation of answer and third is citations. If required, then give in table format.",
    agent=writer_rag,
    tools=[tool],  # Ensure 'tool' is appropriate for the task
    async_execution=False,
    output_file="new-blog-post.md",  # Specify the desired output file path
)

rag_task = Task(
    description=(
        "Answer the Give query: {query} like RAG application of using given context: {context} "
        "Focus on the latest trends."
        "The answer should be easy to understand, engaging, and positive."
        "Also Show source of content That use to generate generate answer."
        "All source are also show in citation and each citation have number and in end there is map of citation number and source."
    ),
    expected_output="A Give normal length answer if user asked something specific like small or big or or more this some type of word then give answer according to that length on {query} advancements formatted as JSON only in which it has three field first is Answer in which generated answer is written and second field is context in which the context value that are used to for generation of answer and third is citations. If required, then give in table format.",
    agent=rag_agent,
    async_execution=False,
    # output_file="new-blog-post.md",  # Specify the desired output file path
)
