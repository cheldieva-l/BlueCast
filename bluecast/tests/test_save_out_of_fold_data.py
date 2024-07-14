import os
import tempfile

import numpy as np
import pandas as pd
import pytest

from bluecast.config.training_config import TrainingConfig
from bluecast.general_utils.general_utils import save_out_of_fold_data


def test_save_out_of_fold_data_regression():
    # Create mock data for oof_data and y_hat
    oof_data = pd.DataFrame({"feature1": [1, 2, 3], "feature2": [4, 5, 6]})
    y_hat = pd.Series([0.1, 0.2, 0.3])
    y_true = pd.Series([0.1, 0.2, 0.3])

    # Create a temporary directory to store the file
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a TrainingConfig instance with the temporary directory as the path
        training_config = TrainingConfig(
            global_random_state=42, out_of_fold_dataset_store_path=tmpdir + "/"
        )

        # Call the function to save out of fold data
        save_out_of_fold_data(
            oof_data, y_hat, y_true, "target_col_name", "regression", training_config
        )

        # Construct the expected file path
        expected_file_path = os.path.join(
            training_config.out_of_fold_dataset_store_path,
            f"oof_data_{training_config.global_random_state}.parquet",
        )

        # Check if the file was created
        assert os.path.exists(expected_file_path), "Output file was not created."

        # Read the file back and check its contents
        saved_oof_data = pd.read_parquet(expected_file_path)
        expected_oof_data = oof_data.copy()
        expected_oof_data["predictions"] = y_hat
        expected_oof_data["target_col_name"] = y_true

        pd.testing.assert_frame_equal(saved_oof_data, expected_oof_data)


def test_save_out_of_fold_data_multiclass():
    # Create mock data for oof_data and y_hat
    oof_data = pd.DataFrame({"feature1": [1, 2, 3], "feature2": [4, 5, 6]})
    y_hat = np.array([[0.1, 0.7, 0.2], [0.2, 0.5, 0.3], [0.3, 0.4, 0.3]])
    y_true = np.asarray([1, 0, 1])

    # Create a temporary directory to store the file
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a TrainingConfig instance with the temporary directory as the path
        training_config = TrainingConfig(
            global_random_state=42, out_of_fold_dataset_store_path=tmpdir + "/"
        )

        # Call the function to save out of fold data
        save_out_of_fold_data(
            oof_data, y_hat, y_true, "target_col_name", "multiclass", training_config
        )

        # Construct the expected file path
        expected_file_path = os.path.join(
            training_config.out_of_fold_dataset_store_path,
            f"oof_data_{training_config.global_random_state}.parquet",
        )

        # Check if the file was created
        assert os.path.exists(expected_file_path), "Output file was not created."

        # Read the file back and check its contents
        saved_oof_data = pd.read_parquet(expected_file_path)
        expected_data = oof_data.copy()
        expected_data["predictions_class_0"] = y_hat[:, 0]
        expected_data["predictions_class_1"] = y_hat[:, 1]
        expected_data["predictions_class_2"] = y_hat[:, 2]
        expected_data["target_col_name"] = y_true

        pd.testing.assert_frame_equal(saved_oof_data, expected_data)


def test_save_out_of_fold_data_binary():
    # Create mock data for oof_data and y_hat
    oof_data = pd.DataFrame({"feature1": [1, 2, 3], "feature2": [4, 5, 6]})
    y_hat = np.array([0.1, 0.9, 0.5])
    y_true = np.asarray([1, 0, 1])

    # Create a temporary directory to store the file
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a TrainingConfig instance with the temporary directory as the path
        training_config = TrainingConfig(
            global_random_state=42, out_of_fold_dataset_store_path=tmpdir + "/"
        )

        # Call the function to save out of fold data
        save_out_of_fold_data(
            oof_data, y_hat, y_true, "target_col_name", "binary", training_config
        )

        # Construct the expected file path
        expected_file_path = os.path.join(
            training_config.out_of_fold_dataset_store_path,
            f"oof_data_{training_config.global_random_state}.parquet",
        )

        # Check if the file was created
        assert os.path.exists(expected_file_path), "Output file was not created."

        # Read the file back and check its contents
        saved_oof_data = pd.read_parquet(expected_file_path)
        expected_data = oof_data.copy()
        expected_data["predictions_class_1"] = y_hat
        expected_data["target_col_name"] = y_true

        pd.testing.assert_frame_equal(saved_oof_data, expected_data)


@pytest.fixture
def sample_oof_data():
    return pd.DataFrame({"feature1": [1, 2, 3], "feature2": [4, 5, 6]})


@pytest.fixture
def training_config():
    return TrainingConfig(out_of_fold_dataset_store_path="test_path/")


def test_save_out_of_fold_data_no_store_path(sample_oof_data, mocker):
    y_hat = pd.Series([0.1, 0.4, 0.8])
    y_true = y_hat
    training_config = TrainingConfig(out_of_fold_dataset_store_path=None)
    mock_to_parquet = mocker.patch("pandas.DataFrame.to_parquet")

    save_out_of_fold_data(
        sample_oof_data, y_hat, y_true, "target_col_name", "regression", training_config
    )

    mock_to_parquet.assert_not_called()
