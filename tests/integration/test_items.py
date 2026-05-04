import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_item(client: AsyncClient, auth_headers):
    resp = await client.post(
        "/api/v1/items/",
        json={"title": "My Item", "description": "A test item"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "My Item"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_items_empty(client: AsyncClient, auth_headers):
    resp = await client.get("/api/v1/items/", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_get_item_not_found(client: AsyncClient, auth_headers):
    resp = await client.get(
        "/api/v1/items/00000000-0000-0000-0000-000000000000",
        headers=auth_headers,
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_and_delete_item(client: AsyncClient, auth_headers):
    create_resp = await client.post(
        "/api/v1/items/",
        json={"title": "To Update"},
        headers=auth_headers,
    )
    item_id = create_resp.json()["id"]

    patch_resp = await client.patch(
        f"/api/v1/items/{item_id}",
        json={"title": "Updated"},
        headers=auth_headers,
    )
    assert patch_resp.status_code == 200
    assert patch_resp.json()["title"] == "Updated"

    delete_resp = await client.delete(f"/api/v1/items/{item_id}", headers=auth_headers)
    assert delete_resp.status_code == 204
