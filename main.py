from typing import Union
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import os
import openai
import time
openai.api_key = os.environ["OPEN_AI_KEY"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

RELIGIONS = ["Christianity", "Islam", "Judaism", "Buddhism", "Hinduism", "Taoism"]

async def query(question: str, religion: str) -> str:
    res = await openai.ChatCompletion.acreate(
        #model="text-davinci-003",
        model="gpt-3.5-turbo",
        max_tokens=128,
        #prompt = f"What is {question} in {religion}"
        messages=[
            {"role": "user", "content": f"According to scripture in {religion}, {question}? One paragraph, max 4 sentences, cite 1 relevant passage. "}
        ]
    )
    return res['choices'][0]['message']['content']
    #return res['choices'][0]['text']

def query_seq(question: str, religion: str) -> str:
    res = openai.ChatCompletion.create(
        #model="text-davinci-003",
        model="gpt-3.5-turbo",
        #prompt = f"What is {question} in {religion}"
        messages=[
            {"role": "user", "content": f"What is {question} in {religion}"}
        ]
    )
    return res['choices'][0]['message']['content']
    #return res['choices'][0]['text']
# def new_openai_question_sequential(religion: str, question: str) -> str:
#     res = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "user", "content": f"In {religion}, what is {question}"}
#         ]
#     )
#     return res['choices'][0]['message']['content']

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/prompts/")
async def create_prompt(question: str):
    response = {"Christianity": "", "Islam": "", "Judaism": ""}
    tasks = []
    start_time = time.time()
    responses = await asyncio.gather(query(question, "Christianity"), query(question, "Islam"), query(question, "Judaism"), query(question, "Buddhism"), query(question, "Hinduism"), query(question, "Taoism"))
    output = {}
    for k, v in zip(RELIGIONS, responses):
        output[k] = v
    print(output)
    print("--- %s Async time---" % (time.time() - start_time))
    start_time = time.time()
    # query_seq(question, "Christianity")
    # query_seq(question, "Islam")
    # query_seq(question, "Judaism")
    # print("--- %s Sequential time---" % (time.time() - start_time))
    return output

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
