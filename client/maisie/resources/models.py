import json
import logging
import urllib.request

from typing import Union
from maisie import BaseAction
from maisie.utils.git import GitProvider
from hashlib import md5

import os

logger = logging.getLogger(__name__)


class Models(BaseAction):
    """Represents an action for managing models."""

    def upload(
        self,
        name: str,
        filename: str,
        hyperparameters: Union[str, dict],
        parameters: Union[str, dict],
        metrics: Union[str, dict],
        private: bool = False,
        dataset_name: str = "",
        dataset_description: str = "",
    ):
        """Posts a single model.

        :param name: name of model to upload
        :param filename: path to file with a model
        :param hyperparameters: dictionary or path to file with hyperparameters
        :param metrics: dictionary or path to file with metrics
        :param private: 
        :param dataset_name:
        :param dataset_description:

        :returns: posted model
        """
        hyperparameters = self._determine_input(hyperparameters)
        parameters = self._determine_input(parameters)
        metrics = self._determine_input(metrics)

        with self.config.session as session:
            files = {}
            try:
                with open(filename, "rb") as f:
                    files["file"] = f.read()
                    checksum = md5(files["file"]).hexdigest()
                # files["file"] = open(filename, "rb").read()
                # checksum = md5(files["file"]).hexdigest()
            except FileNotFoundError:
                logger.error(f"Model `{filename}` could not be found.")

            git = GitProvider(self.config.git_local_repo)
            payload = {
                "name": name,
                "hyperparameters": json.dumps(hyperparameters),
                "parameters": json.dumps(parameters),
                "metrics": json.dumps(metrics),
                "private": private,
                "user_id": 1,
                "project_id": self.config.selected_project,
                "git_active_branch": git.active_branch,
                "git_commit_hash": git.latest_commit,
                "dataset_name": dataset_name,
                "dataset_description": dataset_description,
                "checksum": checksum,
            }
            request = session.post(
                f"{self.config.api_url}/models/", files=files, data=payload
            )

            results = []
            if "data" in request.json():
                results.append(request.json()["data"])
            else:
                logger.error("Could not upload selected model.")

            return results

    def update(self, id: int, data: dict):
        """Update selected model.
        
        :param id: id of the model to put
        :param data: dictionary
        """
        with self.config.session as session:
            pass

    def download(self, id: int, path):
        """Downloads requested model.

        :param id: id of the model to download
        """
        with self.config.session as session:
            request = session.get(f"{self.config.api_url}/models/{id}/")
            request = request.json()
            if (
                ("data") in request
                and "checksum" in request["data"]
                and "_links" in request["data"]
                and "name" in request["data"]
                and "download" in request["data"]["_links"]
            ):
                source_data = session.get(request["data"]["_links"]["download"])
                model_name = request["data"]["name"]
                source_checksum = request["data"]["checksum"]
        if path and model_name:
            model_name = os.path.join(path, model_name)
        response = "Checksums differ"
        with open(model_name, "wb") as model_file:
            for chunk in source_data.iter_content(chunk_size=128):
                model_file.write(chunk)
        with open(model_name, "rb") as model_file:
            local_checksum = md5(model_file.read()).hexdigest()
        # local_checksum = md5(open(model_name, "rb").read()).hexdigest()
        # model_name.close()
        if local_checksum and source_checksum and local_checksum == source_checksum:
            response = "Model downloaded successfully"
        return response

    def get(self, id: int) -> list:
        """Fetches a single model.

        :param id: id of the model to get
        :returns: requested model
        """
        with self.config.session as session:
            request = session.get(f"{self.config.api_url}/models/{id}/")
            results = []
            if "data" in request.json():
                results.append(request.json()["data"])
            else:
                logger.error("Could not fetch any models.")

        return results

    def get_all(self, query=None, page=None, per_page=None):
        """Fetches all models that satisfy some condition.
        
        :param query: query string
        :param page: number of the page used in pagination
        :param per_page: number of the items to be fetched
        :returns: a list of returned models
        """
        results = []
        if not page:
            page = self.config.api_page
        if not per_page:
            per_page = self.config.api_per_page
        with self.config.session as session:
            request = session.get(
                f"{self.config.api_url}/models/",
                params={"page": page, "per_page": per_page},
            )
            if "data" in request.json():
                results = request.json()["data"]
                logger.debug(f"Response body: {results}")
            else:
                logger.error("Could not fetch any models.")

        return results

    def _determine_input(self, value: Union[str, dict]) -> dict:
        if isinstance(value, str):
            value = self._file_into_dict(value)

        return value

    def _file_into_dict(self, filename: str) -> dict:
        try:
            with open(filename, "rb") as filename:
                output = json.load(filename)
        except FileNotFoundError:
            logger.error(f"JSON File `{filename}` could not be found.")
        return output
