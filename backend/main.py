from fastapi import FastAPI


app = FastAPI(title="Jobboard", version="0.1.0")


@app.get("/")
def hello_api():
  return {"detail": "Hello World"}