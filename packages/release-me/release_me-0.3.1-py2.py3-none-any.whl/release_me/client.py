# coding: utf-8
# Copyright (c) 2017 Tadej Borovšak
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mimetypes
import os

import requests


class GithubClientError(Exception):

    def __init__(self, msg):
        self.msg = msg
        super(GithubClientError, self).__init__(msg)

    def __str__(self):
        return "GithubClientError: {}".format(self.msg)


class GithubClient:
    """
    Github client
    """

    API_ENDPOINT = "https://api.github.com"
    UPLOAD_ENDPOINT = "https://uploads.github.com"

    def __init__(self, token):
        self.headers = {
            "User-Agent": "tadeboro",
            "Authorization": "Token {}".format(token),
        }
        self._validate_token()

    def _validate_token(self):
        if self._get(self.API_ENDPOINT).status_code != 200:
            raise GithubClientError("Invalid token")

    def _do_request(self, method, url, **kwargs):
        headers = kwargs.pop("headers", {})
        headers.update(self.headers)
        return method(url, headers=headers, **kwargs)

    def _get(self, url, **kwargs):
        return self._do_request(requests.get, url, **kwargs)

    def _post(self, url, **kwargs):
        return self._do_request(requests.post, url, **kwargs)

    def _delete(self, url, **kwargs):
        return self._do_request(requests.delete, url, **kwargs)

    def get_repo(self, repo):
        resp = self._get("{}/repos/{}".format(self.API_ENDPOINT, repo))
        return resp.status_code == 200, resp.json()

    def get_release(self, repo, tag):
        url = "{}/repos/{}/releases/tags/{}"
        resp = self._get(url.format(self.API_ENDPOINT, repo, tag))
        return resp.status_code == 200, resp.json()

    def create_release(self, repo, tag, name, body):
        data = {
            "tag_name": tag,
            "name": name,
            "body": body,
        }
        url = "{}/repos/{}/releases"
        resp = self._post(url.format(self.API_ENDPOINT, repo), json=data)
        return resp.status_code == 201, resp.json()

    def delete_release(self, repo, release_id):
        url = "{}/repos/{}/releases/{}"
        resp = self._delete(url.format(self.API_ENDPOINT, repo, release_id))
        success = resp.status_code == 204
        return success, {} if success else resp.text

    def upload_asset(self, repo, release_id, asset):
        content_type, _ = mimetypes.guess_type(asset)
        if content_type is None:
            content_type = "application/octet-stream"

        with open(asset, "rb") as handle:
            data = handle.read()
        url = "{}/repos/{}/releases/{}/assets"
        resp = self._post(url.format(self.UPLOAD_ENDPOINT, repo, release_id),
                          data=data, headers={"Content-Type": content_type},
                          params={"name": os.path.basename(asset)})
        return resp.status_code == 201, resp.json()
