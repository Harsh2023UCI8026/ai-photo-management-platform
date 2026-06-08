from fastapi import FastAPI

app = FastAPI(
    title="AI Photo Management Platform"
)

@app.get("/")
def root():
    return {
        "message": "AI Photo Management Platform Running"
    }