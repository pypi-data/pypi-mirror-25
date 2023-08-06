"""
    rest
    ~~~~~~~~~~~~~~~~~~~

    Only use post interface

    :copyright: (c) 2017 by Onni Software Ltd.
    :license: MIT License, see LICENSE for more details

"""

import requests
import gease.exceptions as exceptions


class Api(object):
    """
    A session holder so that each request shares the same token
    """
    def __init__(self, personal_access_token):
        self.__session = requests.Session()
        self.__session.headers.update({
            'Authorization': 'token %s' % personal_access_token})

    def create(self, url, data):
        """
        Create a release

        More information at:
        https://developer.github.com/v3/repos/releases/#create-a-release
        """
        r = self.__session.post(url, json=data)
        if r.status_code == 201:
            return r.json()
        elif r.status_code == 422:
            raise exceptions.ReleaseExistException()
        elif r.status_code == 401:
            response = r.json()
            message = '%s. Please check your gease file' % response['message']
            raise exceptions.AbnormalGithubResponse(message)
        elif r.status_code == 404:
            raise exceptions.RepoNotFoundError()
        else:
            message = 'Github responded with HTTP %s, %s ' % (
                r.status_code, r.text)
            raise exceptions.UnhandledException(message)
