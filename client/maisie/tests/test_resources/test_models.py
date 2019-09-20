import pytest

from maisie.resources.models import Models


models = Models()


def test_correct_upload():
    # correct input
    # test will fail if it raises any kind of unexpected Exception
    models.upload(
        name="some_name",
        filename="params.json",
        hyperparameters="params.json",
        parameters="params.json",
        metrics="params.json",
        dataset_name="dataset_name",
    )


def test_too_long_name():
    # name in database has a limit of 40 characters

    result = models.upload(
        name="111111111111111111111111111111111111111112",
        filename="params.json",
        hyperparameters="params.json",
        parameters="params.json",
        metrics="params.json",
        dataset_name="dataset_name",
    )
    assert (
        result["message"]["name"]
        == "Name of the model must be at most 40 characters long."
    )


def test_not_existing_file():
    filename = "nonexistent_file.json"
    result = models.upload(
        name="some_name",
        filename=filename,
        hyperparameters="params.json",
        parameters="params.json",
        metrics="params.json",
        dataset_name="dataset_name",
    )
    assert result["message"]["file"] == "Missing required parameter in an uploaded file"


# def test_too_big_file():
