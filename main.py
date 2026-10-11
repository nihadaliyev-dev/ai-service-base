from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="ai-service-base")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/add")
def add(a: int, b: int) -> dict[str, int]:
    return {"result": a + b}


@app.get("/multiply")
def multiply(a: int, b: int) -> dict[str, int]:
    return {"result": a * b}


# Pydantic v2 Req Body section


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    temperature: float = Field(default=0.7, ge=0, le=2)
    top_p: float = Field(default=1.0, ge=0, le=1)


class ChatResponse(BaseModel):
    reply: str
    tokens_estimate: int


@app.post("/chat")
def chat(req: ChatRequest) -> ChatResponse:
    # There will be added LLM call
    return ChatResponse(
        reply=f"Echo: {req.message}",
        tokens_estimate=len(req.message.split()),
    )
