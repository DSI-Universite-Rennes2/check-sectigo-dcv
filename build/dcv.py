# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# SPDX-License-Identifier: BSD-3-Clause
# -----------------------------------------------------------------------------
# Authors :
#
#   - Yann 'Ze' Richard <yann.richard à univ-rennes2.fr> - DSI Université Rennes 2
#
# -----------------------------------------------------------------------------
"""Define the cert_manager.dcv.DCV class."""

import re
import logging
from requests.exceptions import HTTPError

from ._endpoint import Endpoint
from ._helpers import paginate, version_hack

LOGGER = logging.getLogger(__name__)

class InvalidValidationMethodError(Exception):
    """An invalid validation method was called"""

class DCV(Endpoint):
    """Query the Sectigo Cert Manager REST API for Domain Control Validation resource (DCV) data."""

    _validation_methods = ['http', 'https', 'cname', 'email']

    def __init__(self, client, api_version="v1"):
        """Initialize the class.

        :param object client: An instantiated cert_manager.Client object
        :param string api_version: The API version to use; the default is "v1"
        """
        super().__init__(client=client, endpoint="/dcv", api_version=api_version)

    def _checkMethod(method):
        if method not in self._validation_methods:
            raise InvalidValidationMethodError(method)

    def _startValidation(self, method, domain):
        """Start Domain Control Validation using the given method.

        :param str method: The submit validation method : http, https, cname or email
        :param str domain: The domain to validate

        :return dict: 'url' of the .well-known/pki-validation file to build and 'firstLine' + 'secondLine' for the content.
        """
        self._checkMethod(method)
        url  = self._url("validation", "start", "domain", {method})
        data = {
            "domain": domain
        }
        result = self._client.post(url, data=data)

        return result.json()

    def startHTTP(self, domain):
        """Start Domain Control Validation using HTTP method.

        :param str domain: The domain to validate

        :return dict: 'url' of the .well-known/pki-validation file to build and 'firstLine' + 'secondLine' for the content.
        """
        return self._startValidation(self, "http", domain)

    def startHTTPS(self, domain):
        """Start Domain Control Validation using HTTPS method.

        :param str domain: The domain to validate

        :return dict: 'url' of the .well-known/pki-validation file to build and 'firstLine' + 'secondLine' for the content.
        """
        return self._startValidation(self, "https", domain)

    def startCName(self, domain):
        """Start Domain Control Validation using CName method.

        :param str domain: The domain to validate

        :return dict: 'host' for the DNS record to add and 'point' for the content of the record.
        """
        return self._startValidation(self, "cname", domain)

    def submitEmail(self, domain):
        """Start Domain Control Validation using Email method.

        :param str domain: The domain to validate

        :return dict: emails list
        """
        return self._startValidation(self, "email", domain)

    def _submitValidation(self, method, domain, email=None):
        """Submit Domain Control Validation using HTTP method.

        :param str method: The submit validation method : http, https, cname or email
        :param str domain: The domain to validate
        :param str email: The email to use with the email method only

        :return dict: dict with 'orderStatus', 'message' and 'status'
        """

        self._checkMethod(method)
        url  = self._url("validation", "submit", "domain", {method})
        data = {
            "domain": domain
        }
        if email:
            data["email"] = email

        result = self._client.post(url, data=data)

        return result.json()

    def submitHTTP(self, domain):
        """Submit Domain Control Validation using HTTP method.

        :param str domain: The domain to validate

        :return dict: dict with 'orderStatus', 'message' and 'status'
        """
        return self._submitValidation(self, "http", domain)

    def submitHTTPS(self, domain):
        """Submit Domain Control Validation using HTTPS method.

        :param str domain: The domain to validate

        :return dict: dict with 'orderStatus', 'message' and 'status'
        """
        return self._submitValidation(self, "https", domain)

    def submitCName(self, domain):
        """Submit Domain Control Validation using CName method.

        :param str domain: The domain to validate

        :return dict: dict with 'orderStatus', 'message' and 'status'
        """
        return self._submitValidation(self, "cname", domain)

    def submitEmail(self, domain, email):
        """Submit Domain Control Validation using Email method.

        :param str domain: The domain to validate
        :param str email: The email used for validation

        :return dict: dict with 'orderStatus', 'message' and 'status'
        """
        return self._submitValidation(self, "email", domain, email)

    @version_hack(service="dcv", version="v2")
    def getStatus(self, domain):
        """Get Validation status

        :param str domain: The domain to validate

        :return dict: dict with 'status', 'orderStatus' and 'expirationDate'
        """
        url  = self._url("validation", "status")
        data = {
            "domain": domain
        }

        result = self._client.post(url, data=data)

        return result.json()

    @paginate
    def search(self, **kwargs):
        """Return Domains Control Validation procedure as a validation statuses.

        The 'size' and 'position' parameters passed as arguments to this function will be used
        by the pagination wrapper to page through results.

            - position      : Position shift
            - size          : Count of entries
            - domain        : Domain
            - org           : Organization ID
            - department    : Department ID
            - dcvStatus     : DCV Status
            - orderStatus   : DCV Order status
            - expiresIn     : Expires in (days)

        :return iter: An iterator object is returned to cycle through the dcv search results
        """
        url    = self._url("/validation")
        result = self._client.get(url, params=kwargs)
        return result.json()

    def clear(self, domain):
        """Reset the parameters of a request for DCV and drop Domain
        validation Status and DCV Order Status of the domain to the
        initial values.

        :param str domain: The domain to validate

        :return dict: dict with 'orderStatus', 'message' and 'status'
        """
        url  = self._url("validation", "clear")
        data = {
            "domain": domain
        }

        result = self._client.post(url, data=data)

        return result.json()
