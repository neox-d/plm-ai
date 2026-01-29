from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI()

# set in Render as AI_GATEWAY_TOKEN (ENV)
import os
AI_GATEWAY_TOKEN = os.getenv("AI_GATEWAY_TOKEN")

class ReviewReq(BaseModel):
    event_id: str
    object_type: str

@app.get("/")
async def root():
    return {"message": "PLM AI Service"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ai/review")
def review(req: ReviewReq, x_api_key: str | None = Header(default=None, alias="X-API-KEY")):
    # Auth
    if AI_GATEWAY_TOKEN and x_api_key != AI_GATEWAY_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # ToDO: call LLM
    suggestion = "approve" if req.object_type.lower() in {"plm", "release"} else "review"
    confidence = 0.86 if suggestion == "approve" else 0.62

    return {
        "suggestion": suggestion,
        "confidence": confidence,
        "summary": f"Suggestion based on object_type={req.object_type}",
        "reasons": [
            "Not watermarked",
            "New release does not follow guidelines"
        ]
    }
