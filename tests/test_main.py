# Unit tests for endpoints

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_shorten_redirect_stats_flow():
    # Step 1: Input sent to the DB
    response = client.post("/shorten", json={"long_url": "https://example.com"})
    assert response.status_code == 200
    data = response.json()
    short_code = data["short_code"]
    print(short_code)
    assert short_code is not None

    # Step 2: Check stats immediately (should exist with click_count=0)
    stats = client.get(f"/stats/{short_code}")
    assert stats.status_code == 200
    stats_data = stats.json()
    assert stats_data["click_count"] == 0
    assert stats_data["last_accessed"] is None or stats_data["last_accessed"] == ""

    # Step 3: Redirect once
    redirect = client.get(f"/{short_code}", follow_redirects=False)
    assert redirect.status_code in (
        200,
        307,
        302,
    )  # depends if you use RedirectResponse or JSON
    # If using RedirectResponse, you can check:
    assert redirect.headers["location"] == "https://example.com"

    # Step 4: Stats should now show click_count=1
    stats = client.get(f"/stats/{short_code}")
    stats_data = stats.json()
    assert stats_data["click_count"] == 1
    assert stats_data["last_accessed"] is not None


def test_invalid_short_code_stats():
    response = client.get("/stats/doesnotexist")
    assert response.status_code == 404
    assert response.json()["detail"] == "Stats not found"
