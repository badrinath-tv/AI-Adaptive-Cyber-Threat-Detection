import pandas as pd

from app.utils.preprocessing import SecurityDataPreprocessor
from app.utils.feature_engineering import SecurityFeatureEngineer


def test_preprocessing():

    data = pd.DataFrame({
        "protocol": ["TCP", "UDP", "TCP"],
        "packets": [10, 20, 30],
        "bytes": [1000, 2000, 3000]
    })

    processor = SecurityDataPreprocessor()

    result = processor.preprocess(
        data,
        categorical_columns=["protocol"],
        numerical_columns=["packets", "bytes"]
    )

    assert not result.empty
    assert result["protocol"].dtype.kind in "iu"


def test_feature_engineering():

    data = pd.DataFrame({
        "Total Fwd Packets": [10, 20],
        "Flow Duration": [100, 200],
        "Total Length of Fwd Packets": [1000, 4000]
    })

    engineer = SecurityFeatureEngineer()

    result = engineer.create_features(data)

    assert "Packets_Per_Time" in result.columns
    assert "Bytes_Per_Time" in result.columns
    assert "Average_Fwd_Packet_Size" in result.columns