import json

from typing import Optional

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class Record(BaseModel):
    sys_id: str
    short_description: Optional[str] = None
    assignment_group: Optional[str] = None


with open('mock_data.json') as f:
    data = json.load(f)

app = FastAPI()


@app.get("/incident/")
def incident_table(q: Optional[str] = None):
    if q:
        for record in data:
            record["q"] = q

    content = { "result": data }
    headers = { "Content-Type": "application/json;charset=UTF-8" }
    return JSONResponse(content=content, headers=headers)


@app.get("/incident/{sys_id}")
def incident_by_id(sys_id):
    inc = data[0]
    inc['sys_id'] = sys_id

    content = { "result": inc }
    headers = { "Content-Type": "application/json;charset=UTF-8" }
    return JSONResponse(content=content, headers=headers)


@app.get("/incident")
def incident_by_number(number: str):
    inc = data[0]
    inc["number"] = number

    content = { "result": inc }
    headers = { "Content-Type": "application/json;charset=UTF-8" }
    return JSONResponse(content=content, headers=headers)


@app.patch("/incident/{sys_id}")
def patch(sys_id, record: Record):
    inc = data[0]
    inc["sys_id"] = sys_id
    inc["short_description"] = record.short_description
    inc["assignment_group"] = record.assignment_group

    content = { "result": inc }
    headers = { "Content-Type": "application/json;charset=UTF-8" }
    return JSONResponse(content=content, headers=headers)


@app.post("/incident", status_code=201)
def post(record: Record):
    inc = {}
    inc["sys_id"] = sys_id
    inc["short_description"] = record.short_description
    inc["assignment_group"] = record.assignment_group

    content = { "result": inc }
    headers = { "Content-Type": "application/json;charset=UTF-8" }
    return JSONResponse(content=content, headers=headers)


@app.put("/incident/{sys_id}", status_code=200)
def put(sys_id, record: Record):
    inc = data[0]
    inc["sys_id"] = sys_id
    inc["short_description"] = record.short_description
    inc["assignment_group"] = record.assignment_group

    content = { "result": inc }
    headers = { "Content-Type": "application/json;charset=UTF-8" }
    return JSONResponse(content=content, headers=headers)


@app.delete("/incident/{sys_id}", status_code=204)
def delete(sys_id):
    headers = { "Content-Type": "application/json;charset=UTF-8" }
    return JSONResponse(content=None, headers=headers)


@app.get("/badtable", status_code=404)
def bad_request():
    raise JSONResponse(content={
        "error": {
            "message": "Not found",
            "detail": "The specified table was not found"
        }
    })