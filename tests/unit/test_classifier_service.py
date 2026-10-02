import pandas as pd

from app.services.detection.classifier_service import ThreatClassifier


DATASET_FILE = (
    "ml/data/processed/binary_dataset.csv"
)


def test_classifier_service():
    df = pd.read_csv(
        DATASET_FILE,
        nrows=5,
        low_memory=False
    )

    classifier = ThreatClassifier()

    feature_columns = classifier.feature_columns

    event = df.iloc[0][feature_columns].to_dict()

    result = classifier.predict(event)

    print("\nClassifier result:")
    print(result)

    assert result["label"] in {
        "BENIGN",
        "ATTACK",
    }

    assert 0.0 <= result["benign_probability"] <= 1.0
    assert 0.0 <= result["attack_probability"] <= 1.0

    assert (
        abs(
            result["benign_probability"]
            + result["attack_probability"]
            - 1.0
        )
        < 0.0001
    )