import json
import re

import uvicorn

from typing import Optional

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class TableNotFoundException(Exception):
    def __init__(self, table: str):
        self.table = table


class Record(BaseModel):
    short_description: Optional[str] = None
    assignment_group: Optional[str] = None


with open('mock_data.json') as f:
    data = json.load(f)

app = FastAPI()


@app.exception_handler(TableNotFoundException)
async def unicorn_exception_handler(request: Request, exc: TableNotFoundException):
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "message": f"Invalid table {exc.table}",
                "detail": None
            },
            "status": "failure"
        }
    )


@app.get("/api/now/table/{table}")
def get_all(
    table: str,
    response: Response,
    number: Optional[str] = None,
    sysparm_fields: Optional[str] = None    
):
    if not table == 'incident':
        raise TableNotFoundException(table=table)

    response.headers["X-Content-Type"] = "application/json;charset=UTF-8"
    
    if sysparm_fields:
        fields = sysparm_fields.split(',')
        result = []
        for n in range(len(data)):
            result.append({})
            for field in fields:
                result[n][field] = data[n][field]
    else:
        result = data

    if number:
        m = re.search(r'(INC[0-9]{7})', number)
        if m:
            for r in result:
                r["number"] = number
            return { "result": result }

    return { "result": result }


@app.get("/api/now/table/incident/{sys_id}")
def get_by_id(sys_id, response: Response):
    response.headers["Content-Type"] = "application/json;charset=UTF-8"
    result = data[0]
    result["sys_id"] = sys_id
    return { "result": result }


@app.patch("/api/now/table/incident/{sys_id}", status_code=200)
def patch(sys_id, record: Record, response: Response):
    result = data[0]
    result["sys_id"] = sys_id
    result["short_description"] = record.short_description
    result["assignment_group"] = record.assignment_group
    response.headers["Content-Type"] = "application/json;charset=UTF-8"
    return { "result": result }


@app.post("/api/now/table/incident", status_code=201)
def post(record: Record, response: Response):
    response.headers["Content-Type"] = "application/json;charset=UTF-8"
    return { "result": {
        "short_description": record.short_description,
        "assignment_group": record.assignment_group
    }}


@app.put("/api/now/table/incident/{sys_id}", status_code=200)
def put(sys_id, record: Record, response: Response):
    response.headers["Content-Type"] = "application/json;charset=UTF-8"
    return { "result": {
        "sys_id": sys_id,
        "short_description": record.short_description,
        "assignment_group": record.assignment_group
    }}


@app.delete("/api/now/table/incident/{sys_id}", status_code=204)
def delete(sys_id):
    return None


if __name__ == '__main__':
    uvicorn.run("mock_api:app", host="0.0.0.0", port=5000, log_level="info", reload=True)