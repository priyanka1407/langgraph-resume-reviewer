# =============================================================================
# Resume Reviewer -- A LangGraph Parallel Workflow Project
# =============================================================================
#
# WHAT THIS DOES:
# A user pastes their resume text and a job description. The system first
# pulls out the key job requirements, then runs 3 specialist reviewers in
# PARALLEL (skills, experience, keywords). A decision node reads all three
# reviews and routes to either MINOR EDITS or a MAJOR REWRITE PLAN.
#
# LANGGRAPH CONCEPTS COVERED:
# 1. State Management (Pydantic) -- resume + job description flow through the graph
# 2. Nodes -- each function does one job (skills check, experience check, etc.)
# 3. Parallel Execution -- 3 specialist nodes run at the same time
# 4. Fan-in -- the decision node waits for all 3 reviews
# 5. Conditional Edges -- routing to minor edits vs major rewrite
# 6. Graph Compilation -- turning the graph definition into a runnable app
#
# GRAPH STRUCTURE:
#
#   START
#     |
#   extract_job_requirements
#     |
#     +---> check_skills_match -------------+
#     |                                     |
#     +---> check_experience_alignment -----+---> decide_resume_action
#     |                                     |         |
#     +---> check_resume_keywords ----------+    (conditional)
#                                              /          \
#                                          minor?        major?
#                                            |              |
#                                 minor_resume_edits   major_resume_rewrite_plan
#                                            |              |
#                                           END            END
#
# HOW TO RUN:
#   python resume_review_graph.py
#
# DEPENDENCIES (same as requirements.txt):
#   langgraph, langchain-openai, python-dotenv, pydantic
#
# =============================================================================

import sys
import operator
from typing import Annotated

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv()


class ResumeState(BaseModel):
    resume_text: str = ""
    job_description: str = ""
    job_requirements: str = ""
    skills_review: str = ""
    experience_review: str = ""
    keywords_review: str = ""
    match_score: int = 0
    needs_major_rewrite: bool = False
    decision_reason: str = ""
    final_recommendation: str = ""
    messages: Annotated[list, operator.add] = []


llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0.3)


def extract_job_requirements(state: ResumeState) -> dict:
    response = llm.invoke(
        f"You are a technical recruiter. Read this job description and list the "
        f"key requirements as short bullet points under three headings: "
        f"Must-have skills, Experience required, Nice-to-have.\n\n"
        f"JOB DESCRIPTION:\n{state.job_description}"
    )
    return {
        "job_requirements": response.content,
        "messages": [f"[extract_job_requirements] Done"]
    }


def check_skills_match(state: ResumeState) -> dict:
    response = llm.invoke(
        f"You are a skills-matching specialist. Compare the resume against the job requirements.\n\n"
        f"JOB REQUIREMENTS:\n{state.job_requirements}\n\n"
        f"RESUME:\n{state.resume_text}\n\n"
        f"List two sections: 'Matching skills' and 'Missing skills'. "
        f"Only count a skill as matching if the resume clearly shows it. "
        f"Keep each section to short bullet points."
    )
    return {
        "skills_review": response.content,
        "messages": [f"[check_skills_match] Done"]
    }


def check_experience_alignment(state: ResumeState) -> dict:
    response = llm.invoke(
        f"You are an experience-alignment specialist. Compare the candidate's work "
        f"experience with what the job requires.\n\n"
        f"JOB REQUIREMENTS:\n{state.job_requirements}\n\n"
        f"RESUME:\n{state.resume_text}\n\n"
        f"Comment on: years of experience vs required, relevance of past roles, "
        f"seniority level, and whether achievements are measurable. "
        f"Keep it under 6 bullet points."
    )
    return {
        "experience_review": response.content,
        "messages": [f"[check_experience_alignment] Done"]
    }


def check_resume_keywords(state: ResumeState) -> dict:
    response = llm.invoke(
        f"You are an ATS (applicant tracking system) keyword specialist.\n\n"
        f"JOB DESCRIPTION:\n{state.job_description}\n\n"
        f"RESUME:\n{state.resume_text}\n\n"
        f"List the most important keywords and phrases from the job description that are "
        f"MISSING from the resume (up to 10). For each, suggest where in the resume it could "
        f"naturally be added. Only suggest keywords the candidate could honestly claim."
    )
    return {
        "keywords_review": response.content,
        "messages": [f"[check_resume_keywords] Done"]
    }


class ResumeDecision(BaseModel):
    match_score: int = Field(description="How well the resume matches the job, 0 to 100")
    needs_major_rewrite: bool = Field(description="True if the resume needs a major rewrite")
    reason: str = Field(description="One sentence explanation of the decision")


decision_llm = llm.with_structured_output(ResumeDecision)


def decide_resume_action(state: ResumeState) -> dict:
    response = decision_llm.invoke(
        f"You are a resume review decision system.\n\n"
        f"Here are three specialist reviews of a resume against a job:\n\n"
        f"SKILLS REVIEW:\n{state.skills_review}\n\n"
        f"EXPERIENCE REVIEW:\n{state.experience_review}\n\n"
        f"KEYWORDS REVIEW:\n{state.keywords_review}\n\n"
        f"Give a match score from 0 to 100. Decide whether the resume needs MINOR edits "
        f"(good fit, small gaps, score 65 or above) or a MAJOR rewrite (big gaps in skills, "
        f"experience, or keywords, score below 65)."
    )
    score = response.match_score
    needs_major = response.needs_major_rewrite
    reason = response.reason

    return {
        "match_score": score,
        "needs_major_rewrite": needs_major,
        "decision_reason": reason,
        "messages": [f"[decide_resume_action] score={score}, major_rewrite={needs_major}"]
    }


def minor_resume_edits(state: ResumeState) -> dict:
    response = llm.invoke(
        f"You are a friendly career coach. This resume is already a good fit for the job "
        f"and only needs small improvements.\n\n"
        f"SKILLS REVIEW: {state.skills_review}\n"
        f"EXPERIENCE REVIEW: {state.experience_review}\n"
        f"KEYWORDS REVIEW: {state.keywords_review}\n\n"
        f"RESUME:\n{state.resume_text}\n\n"
        f"Give 5-8 specific, quick edits as a numbered list. Where useful, show a "
        f"'Before' and 'After' version of a bullet point. End with one encouraging line."
    )
    return {
        "final_recommendation": f"MINOR RESUME EDITS\n{'='*45}\n{response.content}",
        "messages": [f"[minor_resume_edits] Generated minor edits"]
    }


def major_resume_rewrite_plan(state: ResumeState) -> dict:
    response = llm.invoke(
        f"You are an experienced career coach. This resume has significant gaps for the "
        f"target job and needs a major rewrite.\n\n"
        f"JOB REQUIREMENTS: {state.job_requirements}\n"
        f"SKILLS REVIEW: {state.skills_review}\n"
        f"EXPERIENCE REVIEW: {state.experience_review}\n"
        f"KEYWORDS REVIEW: {state.keywords_review}\n\n"
        f"RESUME:\n{state.resume_text}\n\n"
        f"Create a rewrite plan in 4 phases: 1) New summary/headline, 2) Restructure "
        f"skills section, 3) Rewrite experience bullets around job requirements with "
        f"measurable results, 4) Close the gaps (projects, certifications, or learning to add). "
        f"Give concrete actions for each phase. Be honest but supportive."
    )
    return {
        "final_recommendation": f"MAJOR RESUME REWRITE PLAN\n{'='*45}\n{response.content}",
        "messages": [f"[major_resume_rewrite_plan] Generated rewrite plan"]
    }


def route_after_decision(state: ResumeState) -> str:
    if state.needs_major_rewrite:
        return "major"
    else:
        return "minor"


graph = StateGraph(ResumeState)

graph.add_node("extract_job_requirements", extract_job_requirements)
graph.add_node("check_skills_match", check_skills_match)
graph.add_node("check_experience_alignment", check_experience_alignment)
graph.add_node("check_resume_keywords", check_resume_keywords)
graph.add_node("decide_resume_action", decide_resume_action)
graph.add_node("minor_resume_edits", minor_resume_edits)
graph.add_node("major_resume_rewrite_plan", major_resume_rewrite_plan)

graph.add_edge(START, "extract_job_requirements")

graph.add_edge("extract_job_requirements", "check_skills_match")
graph.add_edge("extract_job_requirements", "check_experience_alignment")
graph.add_edge("extract_job_requirements", "check_resume_keywords")

graph.add_edge("check_skills_match", "decide_resume_action")
graph.add_edge("check_experience_alignment", "decide_resume_action")
graph.add_edge("check_resume_keywords", "decide_resume_action")

graph.add_conditional_edges(
    "decide_resume_action",
    route_after_decision,
    {
        "minor": "minor_resume_edits",
        "major": "major_resume_rewrite_plan",
    }
)

graph.add_edge("minor_resume_edits", END)
graph.add_edge("major_resume_rewrite_plan", END)

app = graph.compile()


def run_resume_review(resume_text: str, job_description: str):
    print("=" * 55)
    print("  RESUME REVIEWER")
    print("=" * 55)

    result = app.invoke({
        "resume_text": resume_text,
        "job_description": job_description,
        "messages": [],
    })

    print("\n" + "-" * 55)
    print("  SPECIALIST REVIEWS")
    print("-" * 55)
    print(f"\n[SKILLS]\n{result['skills_review']}")
    print(f"\n[EXPERIENCE]\n{result['experience_review']}")
    print(f"\n[KEYWORDS]\n{result['keywords_review']}")

    print("\n" + "=" * 55)
    print(f"  MATCH SCORE: {result['match_score']}/100")
    print(f"  DECISION: {'Major rewrite' if result['needs_major_rewrite'] else 'Minor edits'}")
    print(f"  WHY: {result['decision_reason']}")
    print("=" * 55)
    print(f"\n{result['final_recommendation']}")

    print("\n" + "-" * 55)
    print("  MESSAGE LOG")
    print("-" * 55)
    for msg in result["messages"]:
        print(f"  {msg}")

    return result


SAMPLE_RESUME = """Jane Doe - Software Engineer
Experience:
- Software Engineer, Acme Corp (2021-2024): Built REST APIs in Python and Flask.
  Wrote unit tests and fixed production bugs. Worked with PostgreSQL.
- Intern, Beta Labs (2020): Built internal dashboards with JavaScript.
Skills: Python, Flask, SQL, Git, JavaScript
Education: B.Tech Computer Science, 2021"""

SAMPLE_JOB = """AI Engineer
We are looking for an AI Engineer with 3+ years of Python experience.
Must have: Python, LLM APIs (OpenAI or similar), LangChain or LangGraph,
RAG pipelines, vector databases, FastAPI, Docker.
Nice to have: AWS, prompt engineering, evaluation of LLM outputs."""


def read_multiline(prompt: str) -> str:
    print(f"  {prompt} (type END on its own line when done)")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    return "\n".join(lines).strip()


if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("  RESUME REVIEWER")
    print("=" * 55)
    print("\n  Paste your resume and a job description and I'll")
    print("  recommend improvements.")
    print("  Type 'sample' to try a built-in example, or 'quit' to exit.\n")

    while True:
        choice = input("  Press Enter to start, or type sample/quit > ").strip().lower()

        if choice in ("quit", "exit", "q"):
            print("\n  Good luck with your applications. Goodbye!\n")
            break

        if choice == "sample":
            run_resume_review(SAMPLE_RESUME, SAMPLE_JOB)
            print("\n")
            continue

        resume = read_multiline("Paste your RESUME text")
        job = read_multiline("Paste the JOB DESCRIPTION")

        if not resume or not job:
            print("  Both resume and job description are needed.\n")
            continue

        run_resume_review(resume, job)
        print("\n")
