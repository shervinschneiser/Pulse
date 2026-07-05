from fastapi import FastAPI

app = FastAPI(
    title="Pulse",
    version="0.1.0",
)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Pulse API"}
