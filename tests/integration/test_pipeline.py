import pandas as pd

from app.database.database import SessionLocal, init_database
from app.services.detection.pipeline_service import (
    DetectionPipeline,
)


DATASET_FILE = (
    "ml/data/processed/binary_dataset.csv"
)


def test_detection_pipeline():
    init_database()

    df = pd.read_csv(
        DATASET_FILE,
        nrows=5,
        low_memory=False,
    )

    pipeline = DetectionPipeline()

    feature_columns = (
        pipeline.classifier.feature_columns
    )

    event = (
        df.iloc[0][feature_columns]
        .to_dict()
    )

    # Run complete detection pipeline
    result = pipeline.analyze(event)

    print("\nDetection Pipeline Result:")
    print(result)

    assert "classification" in result
    assert "anomaly" in result
    assert "risk" in result
    assert "response" in result

    assert result["classification"]["label"] in {
        "BENIGN",
        "ATTACK",
    }

    assert isinstance(
        result["anomaly"]["is_anomaly"],
        bool,
    )

    assert 0 <= result["risk"]["risk_score"] <= 100

    assert result["risk"]["risk_level"] in {
        "LOW",
        "MEDIUM",
        "HIGH",
    }

    assert result["response"]["risk_level"] == (
        result["risk"]["risk_level"]
    )

    # Persist detection result
    db = SessionLocal()

    try:
        saved_event = pipeline.save_result(
            db,
            result,
        )

        print("\nSaved Database Event:")
        print(
            f"ID          : {saved_event.id}"
        )
        print(
            f"Classification: "
            f"{saved_event.classification}"
        )
        print(
            f"Risk Score  : "
            f"{saved_event.risk_score}"
        )
        print(
            f"Risk Level  : "
            f"{saved_event.risk_level}"
        )
        print(
            f"Actions     : "
            f"{saved_event.response_actions}"
        )

        assert saved_event.id is not None

        assert (
            saved_event.classification
            == result["classification"]["label"]
        )

        assert (
            saved_event.risk_level
            == result["risk"]["risk_level"]
        )

        assert (
            saved_event.response_actions
            == result["response"]["actions"]
        )

    finally:
        db.close()