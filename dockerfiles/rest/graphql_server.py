import json
import os
from typing import Any, List, Optional

import databases
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

database = databases.Database(os.environ["DB_URI"])


class GraphQLRequest(BaseModel):
    query: str
    variables: Optional[str]


class GraphQLResponse(BaseModel):
    data: Any
    errors: Optional[List[Any]]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/hello")
def world():
    return "world"


@app.post("/rpc/graphql", response_model=GraphQLResponse)
async def graphql(request: GraphQLRequest):
    row = await database.fetch_one(
        query="select gql.resolve(:query, :variables)",
        values={"query": request.query, "variables": request.variables},
    )
    # Unwrap Optional[Row] -> Row
    assert row is not None
    json_serialized = row["resolve"]
    return json.loads(json_serialized)
