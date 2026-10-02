"""
Feature engineering utilities for cybersecurity events.
"""

from __future__ import annotations

import pandas as pd


class SecurityFeatureEngineer:
    """
    Creates derived features from security-event data.
    """

    def create_features(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:

        if df.empty:
            raise ValueError("Input DataFrame is empty.")

        df = df.copy()

        # Flow-rate features
        if {
            "Total Fwd Packets",
            "Flow Duration"
        }.issubset(df.columns):

            duration = df["Flow Duration"].replace(
                0,
                1
            )

            df["Packets_Per_Time"] = (
                df["Total Fwd Packets"] / duration
            )

        if {
            "Total Length of Fwd Packets",
            "Flow Duration"
        }.issubset(df.columns):

            duration = df["Flow Duration"].replace(
                0,
                1
            )

            df["Bytes_Per_Time"] = (
                df["Total Length of Fwd Packets"]
                / duration
            )

        # Packet-size feature
        if {
            "Total Length of Fwd Packets",
            "Total Fwd Packets"
        }.issubset(df.columns):

            packets = df["Total Fwd Packets"].replace(
                0,
                1
            )

            df["Average_Fwd_Packet_Size"] = (
                df["Total Length of Fwd Packets"]
                / packets
            )

        return df

    def select_features(
        self,
        df: pd.DataFrame,
        features: list[str]
    ) -> pd.DataFrame:

        available_features = [
            feature
            for feature in features
            if feature in df.columns
        ]

        if not available_features:
            raise ValueError(
                "None of the requested features exist in the dataset."
            )

        return df[available_features].copy()