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

from __future__ import print_function

import argparse
import json
import logging
import os
import sys

from release_me.client import GithubClient


class ArgParser(argparse.ArgumentParser):
    """
    Argument parser that displays help on error
    """

    def error(self, message):
        sys.stderr.write("error: {}\n".format(message))
        self.print_help()
        sys.exit(2)

    def add_subparsers(self):
        # Workaround for http://bugs.python.org/issue9253
        subparsers = super(ArgParser, self).add_subparsers()
        subparsers.required = True
        subparsers.dest = "command"
        return subparsers


def _get_client(logger):
    try:
        token = os.environ["RELEASEME_TOKEN"]
        client = GithubClient(token)
    except client.GithubClientError as error:
        logger.error(error)
        sys.exit(1)
    except KeyError:
        logger.error("Missing access token. Set RELEASEME_TOKEN env variable.")
        sys.exit(1)
    return client


def check_repo(client, logger, repo):
    repo_exists, _ = client.get_repo(repo)
    if not repo_exists:
        logger.error("Invalid repository '{}'".format(repo))
        sys.exit(1)


def create_release(client, logger, args):
    """
    Create new Github release.
    """
    check_repo(client, logger, args.repo)

    logger.info("Creating release for tag {} {}".format(args.repo, args.tag))
    name = args.tag if args.name is None else args.name
    notes = args.notes.read()
    created, response = client.create_release(args.repo, args.tag, name, notes)
    if not created:
        logger.error(response)
        sys.exit(1)

    release_id = response["id"]
    assets = [] if args.asset is None else args.asset
    for asset in assets:
        logger.info("Uploading asset {} for {}".format(asset, release_id))
        success, response = client.upload_asset(args.repo, release_id, asset)
        if not success:
            logger.error(response)


def delete_release(client, logger, args):
    """
    Delete Github release
    """
    check_repo(client, logger, args.repo)

    logger.info("Getting release for tag {}".format(args.tag))
    success, release = client.get_release(args.repo, args.tag)
    if not success:
        logger.error("Release {} {} not found.".format(args.repo, args.tag))
        sys.exit(1)

    logger.info("Deleting release for tag {}".format(args.tag))
    deleted, response = client.delete_release(args.repo, release["id"])
    if not deleted:
        logger.error(response)
        sys.exit(1)


def get_release(client, logger, args):
    """
    Get Github release for selected tag
    """
    check_repo(client, logger, args.repo)

    logger.info("Getting release for tag {}".format(args.tag))
    success, release = client.get_release(args.repo, args.tag)
    if not success:
        logger.error("Release {} {} not found.".format(args.repo, args.tag))
        sys.exit(1)
    print(
        json.dumps(release, indent=2, separators=(",", ": "), sort_keys=True)
    )


def add_assets(client, logger, args):
    """
    Upload additional assets to selected release.
    """
    check_repo(client, logger, args.repo)

    logger.info("Getting release for tag {}".format(args.tag))
    success, release = client.get_release(args.repo, args.tag)
    if not success:
        logger.error("Release {} {} not found.".format(args.repo, args.tag))
        sys.exit(1)

    release_id = release["id"]
    assets = [] if args.asset is None else args.asset
    for asset in assets:
        logger.info("Uploading asset {} for {}".format(asset, release_id))
        success, response = client.upload_asset(args.repo, release_id, asset)
        if not success:
            logger.error(response)


def _add_common_params(parser):
    parser.add_argument("-r", "--repo", required=True,
                        help="Github repo (eg. tadeboro/release-me)")
    parser.add_argument("-t", "--tag", required=True,
                        help="Existing git tag name")


def _create_parser():
    parser = ArgParser(description="Github release helper",
                       formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers()

    get_p = subparsers.add_parser("get", help="Get existing release")
    get_p.set_defaults(func=get_release)
    _add_common_params(get_p)

    create_p = subparsers.add_parser("create", help="Create new release")
    create_p.add_argument("-n", "--notes", required=True,
                          type=argparse.FileType("r"),
                          help="Path to release notes file")
    create_p.add_argument("-a", "--asset", help="Asset to upload",
                          action="append", default=[])
    create_p.add_argument("-l", "--name", default=None,
                          help="Release name (if not specified, tag is used)")
    create_p.set_defaults(func=create_release)
    _add_common_params(create_p)

    delete_p = subparsers.add_parser("delete", help="Delete release")
    delete_p.set_defaults(func=delete_release)
    _add_common_params(delete_p)

    add_assets_p = subparsers.add_parser(
        "add-asset", help="Add additional assets to existing release"
    )
    add_assets_p.add_argument("-a", "--asset", help="Asset to upload",
                          action="append", default=[])
    add_assets_p.set_defaults(func=add_assets)
    _add_common_params(add_assets_p)

    return parser


def _setup_logging():
    fmt_stream = logging.Formatter("[%(levelname)s] - %(message)s")
    handler_stream = logging.StreamHandler()
    handler_stream.setFormatter(fmt_stream)
    handler_stream.setLevel(logging.INFO)

    log = logging.getLogger("fcoclient")
    log.addHandler(handler_stream)
    log.setLevel(logging.DEBUG)

    return log


def main():
    parser = _create_parser()
    args = parser.parse_args()

    logger = _setup_logging()
    client = _get_client(logger)

    args.func(client, logger, args)
