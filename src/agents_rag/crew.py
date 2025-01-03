from crewai import Crew, Process

from agents_rag.agents import rag_agent, writer_rag
from agents_rag.tasks import rag_task, write_rag_task


def get_crew_response(query=None, context=None, url=None):
    if url != "None":
        print("in crwe url")
        ## Forming the tech focused crew with some enhanced configuration
        crew_search = Crew(
            agents=[writer_rag],
            tasks=[write_rag_task],
            process=Process.sequential,
        )

        ## starting the task execution process wiht enhanced feedback
        result_web = crew_search.kickoff(
            inputs={
                "query": f"{query}",
                "url": f"{url}",
            }
        )
        print(result_web)

        result_web = result_web.removeprefix("```json")
        result_web = result_web.removesuffix("```")
        result_web = result_web.replace("```", "")

        return result_web
    else:
        print("In crew else")
        ## Forming the tech focused crew with some enhanced configuration
        crew_rag = Crew(
            agents=[rag_agent],
            tasks=[rag_task],
            process=Process.sequential,
        )

        ## starting the task execution process wiht enhanced feedback
        result_rag = crew_rag.kickoff(
            inputs={
                "query": f"{query}",
                "context": f"{context}",
            }
        )

        result_rag = result_rag.removeprefix("```json")
        result_rag = result_rag.removesuffix("```")
        result_rag = result_rag.replace("```", "")

        return result_rag
