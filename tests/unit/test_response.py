from app.services.response.response_service import ResponseService


def test_low_risk_response():
    service = ResponseService()

    result = service.generate_response("LOW")

    assert result["risk_level"] == "LOW"
    assert result["actions"] == [
        "LOG_EVENT",
    ]
    assert result["executed"] is False
    assert result["simulation"] is True


def test_medium_risk_response():
    service = ResponseService()

    result = service.generate_response("MEDIUM")

    assert result["risk_level"] == "MEDIUM"
    assert result["actions"] == [
        "LOG_EVENT",
        "ALERT_ANALYST",
    ]
    assert result["executed"] is False
    assert result["simulation"] is True


def test_high_risk_response():
    service = ResponseService()

    result = service.generate_response("HIGH")

    assert result["risk_level"] == "HIGH"
    assert result["actions"] == [
        "LOG_EVENT",
        "CREATE_INCIDENT",
        "SIMULATE_CONTAINMENT",
    ]
    assert result["executed"] is False
    assert result["simulation"] is True


def test_case_insensitive_risk_level():
    service = ResponseService()

    result = service.generate_response("high")

    assert result["risk_level"] == "HIGH"


def test_invalid_risk_level():
    service = ResponseService()

    try:
        service.generate_response("UNKNOWN")
        assert False
    except ValueError:
        assert True