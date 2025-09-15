# tests/test_api.py
from fastapi.testclient import TestClient
from app.main import app
from app.security import API_KEY

client = TestClient(app)

# Use a global variable to store the ID of the created item
created_item_id = None

def test_full_api_lifecycle():
    """
    Integration test for the complete CRUD lifecycle of an item.
    """
    global created_item_id
    
    headers = {"X-API-Key": API_KEY}
    
    # 1. CREATE an item
    response = client.post(
        "/items/",
        headers=headers,
        json={"title": "Integration Test Book", "author": "Tester"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Integration Test Book"
    created_item_id = data["id"]
    assert created_item_id is not None

    # 2. READ the created item
    response = client.get(f"/items/{created_item_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Integration Test Book"
    
    # 3. READ list of items
    response = client.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

    # 4. UPDATE the item
    response = client.put(
        f"/items/{created_item_id}",
        headers=headers,
        json={"title": "Updated Test Book", "author": "Updated Tester"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Test Book"
    
    # 5. DELETE the item
    response = client.delete(f"/items/{created_item_id}", headers=headers)
    assert response.status_code == 204
    
    # 6. VERIFY item is deleted
    response = client.get(f"/items/{created_item_id}")
    assert response.status_code == 404
