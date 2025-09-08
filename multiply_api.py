from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Multiply API")

class Numbers(BaseModel):
    a: float
    b: float
    c: float

@app.post("/multiply")
def multiply_numbers(nums: Numbers):
    result = nums.a * nums.b * nums.c
    return {"status": "success", "result": result}
