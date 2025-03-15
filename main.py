from tkinter.font import names

import uvicorn
from fastapi import FastAPI
from db.views import router as db_router

app = FastAPI()

app.include_router(db_router)


@app.get("/")
async def root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
