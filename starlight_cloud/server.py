import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any

import openai


#================================================
# CONFIG
#================================================

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("[WARN] OPENAI_API_KEY is missing — server will not function.")
openai.api_key = OPENAI_API_KEY


#================================================
# MODELS
#================================================

class EmbedRequest(BaseModel):
    texts: List[str]


class ReasonRequest(BaseModel):
    user_message: str
    intent: str
    episodic_memories: List[str] = []
    meta: Dict[str, Any] = {}


class ReasonResponse(BaseModel):
    reply: str
    used_memories: int
    model: str = "gpt-4.1-mini"


#================================================
# FASTAPI APP
#================================================

app = FastAPI(
    title="Starlight Cloud Server",
    description="Cloud reasoning and embedding for Starlight Hybrid AI",
    version="1.0.0"
)


#================================================
# ROUTES
#================================================

@app.get("/health")
def health():
    return {"status": "ok", "service": "starlight-cloud"}


@app.post("/embed")
def embed_text(req: EmbedRequest):
    """
    Generate text embeddings using OpenAI.
    USB Starlight calls this from cloud_client.cloud_embed()
    """
    try:
        response = openai.embeddings.create(
            model="text-embedding-3-small",
            input=req.texts
        )
        vectors = [d.embedding for d in response.data]
        return {"embeddings": vectors}
    except Exception as e:
        return {"error": str(e), "embeddings": []}


@app.post("/reason")
def reason(req: ReasonRequest):
    """
    Hybrid reasoning endpoint.
    USB sends:
      - user_message
      - intent
      - episodic_memories
      - meta
    Cloud returns structured reasoning.
    """
    memory_blob = "\n".join(req.episodic_memories)

    system_prompt = f"""
You are Starlight Cloud Intelligence — a reasoning module.
You receive:
1. User message
2. Detected intent
3. Episodic memory snippets
4. Metadata

Your job:
- Respond clearly
- Use memory when relevant
- Be warm, precise, and helpful
"""

    final_prompt = f"""
User message:
{req.user_message}

Intent:
{req.intent}

Relevant memories:
{memory_blob}

Metadata:
{req.meta}
"""

    try:
        r = openai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": final_prompt},
            ]
        )
        reply = r.choices[0].message.content
    except Exception as e:
        reply = f"[Cloud reasoning error] {str(e)}"

    return ReasonResponse(
        reply=reply,
        used_memories=len(req.episodic_memories),
        model="gpt-4.1-mini"
    )


@app.get("/echo")
def echo(x: str):
    return {"echo": x}


#================================================
# LOCAL DEV MODE
#================================================

if __name__ == "__main__":
    uvicorn.run("server:app",
                host="0.0.0.0",
                port=7860,
                reload=True)
