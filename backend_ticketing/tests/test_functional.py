def test_homepage(app):
    res = app.get("/", status=200)
    assert "Whiish Bus Ticketing API" in res.text


def test_get_buses(app):
    res = app.get("/api/buses", status=200)
    data = res.json
    assert isinstance(data, list)
    assert data[0]['name'] == "Sinar Jaya"
