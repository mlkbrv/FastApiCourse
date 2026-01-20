import pytest
from httpx import AsyncClient


async def create_post(body:str, async_client:AsyncClient) -> dict:
    response = await async_client.post("/post", json={"body": body})
    return response.json()

async def create_comment(body:str,post_id: int, async_client:AsyncClient) -> dict:
    response = await async_client.post("/comment", json={"body": body, "post_id": post_id})
    return response.json()

@pytest.fixture()
async def created_post(async_client:AsyncClient):
    return await create_post("Test Post", async_client=async_client)

@pytest.fixture()
async def created_comment(async_client:AsyncClient,created_post:dict):
    return await create_comment("Test Comment",created_post["id"], async_client=async_client)

@pytest.mark.anyio
async def test_create_post(async_client:AsyncClient):
    body = "Test Post"
    response = await async_client.post("/post", json={"body": body})
    assert response.status_code == 201
    assert {"id":0, "body":body}.items() <= response.json().items()

@pytest.mark.anyio
async def test_create_post_missing_data(async_client:AsyncClient):
    response = await async_client.post("/post", json={})
    assert response.status_code == 422

@pytest.mark.anyio
async def test_get_all_posts(async_client:AsyncClient, created_post:dict):
    response = await async_client.get("/post")
    assert response.status_code == 200
    assert response.json() == [created_post]

@pytest.mark.anyio
async def test_create_comment(async_client: AsyncClient, created_post: dict):
    body = "Test Comment"
    payload = {"body": body, "post_id": created_post["id"]}
    response = await async_client.post("/comment", json=payload)

    assert response.status_code == 201
    assert response.json()["body"] == body
    assert response.json()["post_id"] == created_post["id"]

@pytest.mark.anyio
async def test_get_comments_on_post(async_client: AsyncClient, created_post: dict, created_comment: dict):
    response = await async_client.get(f"/post/{created_post['id']}/comment")
    assert response.status_code == 200
    assert response.json() == [created_comment]
