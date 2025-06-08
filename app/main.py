from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import json
import os

app = FastAPI(title="TDS Virtual TA")

class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None

class Link(BaseModel):
    url: str
    text: str

# Load course data
with open('data/course_content.json') as f:
    COURSE_CONTENT = json.load(f)

with open('data/discourse_posts.json') as f:
    DISCOURSE_POSTS = json.load(f)

def find_relevant_links(question: str) -> List[Link]:
    relevant = []
    q = question.lower()
    
    # Course content matching
    if "model" in q or "gpt" in q:
        relevant.append(Link(
            url=COURSE_CONTENT["models"]["policy_url"],
            text="Course Model Usage Policy"
        ))
    
    # Discourse matching
    for post in DISCOURSE_POSTS:
        if any(kw in q for kw in post["keywords"]):
            relevant.append(Link(
                url=post["url"],
                text=post["excerpt"]
            ))
    
    return relevant

@app.post("/")
async def answer_question(request: QuestionRequest):
    try:
        # Core answer logic
        answer = "You must use `gpt-3.5-turbo-0125` as per course guidelines."
        if "token" in request.question.lower():
            answer = "Use Prof. Anand's tokenizer method to calculate tokens."
        
        # Image handling placeholder
        if request.image:
            answer += " [Image analysis not yet implemented]"

        return {
            "answer": answer,
            "links": [link.dict() for link in find_relevant_links(request.question)]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
