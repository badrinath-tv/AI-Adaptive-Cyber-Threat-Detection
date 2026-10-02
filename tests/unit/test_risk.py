from app.services.risk.risk_service import RiskEngine


def test_low_risk():
    engine = RiskEngine()

    result = engine.calculate_risk(
        attack_probability=0.05,
        anomaly_score=0.30,
    )

    assert result["risk_level"] == "LOW"
    assert 0 <= result["risk_score"] < 40


def test_medium_risk():
    engine = RiskEngine()

    result = engine.calculate_risk(
        attack_probability=0.55,
        anomaly_score=0.10,
    )

    assert result["risk_level"] == "MEDIUM"
    assert 40 <= result["risk_score"] < 70


def test_high_risk():
    engine = RiskEngine()

    result = engine.calculate_risk(
        attack_probability=0.95,
        anomaly_score=-0.05,
    )

    assert result["risk_level"] == "HIGH"
    assert result["risk_score"] >= 70


def test_probability_validation():
    engine = RiskEngine()

    try:
        engine.calculate_risk(
            attack_probability=1.5,
            anomaly_score=0.10,
        )
        assert False
    except ValueError:
        assert True


def test_weights_are_normalized():
    engine = RiskEngine(
        classifier_weight=7,
        anomaly_weight=3,
    )

    assert engine.classifier_weight == 0.7
    assert engine.anomaly_weight == 0.3