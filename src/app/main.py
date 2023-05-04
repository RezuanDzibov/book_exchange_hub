from fastapi import FastAPI

app = FastAPI(title="Book Exchange Hub")


@app.get("/healthcheck")
async def healthcheck():
    return "OK"
