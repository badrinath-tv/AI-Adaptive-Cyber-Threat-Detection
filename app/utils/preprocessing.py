"""
Data preprocessing utilities for the
AI-Powered Adaptive Cyber Threat Detection & Response System.
"""

from __future__ import annotations

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler


class SecurityDataPreprocessor:
    """
    Handles cleaning and preprocessing of structured
    cybersecurity event data.
    """

    def __init__(self):
        self.label_encoders: dict[str, LabelEncoder] = {}
        self.scaler = StandardScaler()
        self.feature_columns: list[str] = []

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean a raw security-event DataFrame.
        """

        if df.empty:
            raise ValueError("Input DataFrame is empty.")

        # Remove duplicate records
        df = df.drop_duplicates().copy()

        # Replace infinite values
        df = df.replace([np.inf, -np.inf], np.nan)

        # Fill numerical missing values with median
        numeric_columns = df.select_dtypes(
            include=[np.number]
        ).columns

        for column in numeric_columns:
            df[column] = df[column].fillna(df[column].median())

        # Fill categorical missing values
        categorical_columns = df.select_dtypes(
            exclude=[np.number]
        ).columns

        for column in categorical_columns:
            if not df[column].mode().empty:
                df[column] = df[column].fillna(
                    df[column].mode()[0]
                )
            else:
                df[column] = df[column].fillna("unknown")

        return df

    def encode_categorical(
        self,
        df: pd.DataFrame,
        columns: list[str]
    ) -> pd.DataFrame:
        """
        Encode categorical columns using LabelEncoder.
        """

        df = df.copy()

        for column in columns:

            if column not in df.columns:
                continue

            encoder = LabelEncoder()

            df[column] = encoder.fit_transform(
                df[column].astype(str)
            )

            self.label_encoders[column] = encoder

        return df

    def scale_features(
        self,
        df: pd.DataFrame,
        columns: list[str],
        fit: bool = True
    ) -> pd.DataFrame:
        """
        Scale numerical features using StandardScaler.
        """

        df = df.copy()

        existing_columns = [
            column
            for column in columns
            if column in df.columns
        ]

        if not existing_columns:
            return df

        if fit:
            df[existing_columns] = self.scaler.fit_transform(
                df[existing_columns]
            )
        else:
            df[existing_columns] = self.scaler.transform(
                df[existing_columns]
            )

        self.feature_columns = existing_columns

        return df

    def preprocess(
        self,
        df: pd.DataFrame,
        categorical_columns: list[str] | None = None,
        numerical_columns: list[str] | None = None
    ) -> pd.DataFrame:
        """
        Complete preprocessing pipeline.
        """

        df = self.clean_data(df)

        categorical_columns = categorical_columns or []
        numerical_columns = numerical_columns or []

        if categorical_columns:
            df = self.encode_categorical(
                df,
                categorical_columns
            )

        if numerical_columns:
            df = self.scale_features(
                df,
                numerical_columns
            )

        return df