from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Request body model
class Numbers(BaseModel):
    a: int
    b: int
    c: int

# Root health check
@app.get("/")
def root():
    return {"message": "API is running! Use /multiply"}

# GET example (simple demo)
@app.get("/multiply")
def multiply_get(a: int, b: int, c: int):
    """
    Multiply using GET query params:
    /multiply?a=2&b=3&c=4
    """
    result = a * b * c
    return {"a": a, "b": b, "c": c, "result": result}

# POST example (JSON body)
@app.post("/multiply")
def multiply_post(numbers: Numbers):
    """
    Multiply using POST with JSON body:
    {"a":2,"b":3,"c":4}
    """
    result = numbers.a * numbers.b * numbers.c
    return {"a": numbers.a, "b": numbers.b, "c": numbers.c, "result": result}

# PUT example (update-style demo)
@app.put("/multiply")
def multiply_put(numbers: Numbers):
    """
    Multiply using PUT with JSON body:
    {"a":2,"b":3,"c":4}
    """
    result = numbers.a * numbers.b * numbers.c
    return {
        "operation": "updated multiplication",
        "a": numbers.a,
        "b": numbers.b,
        "c": numbers.c,
        "result": result
    }
