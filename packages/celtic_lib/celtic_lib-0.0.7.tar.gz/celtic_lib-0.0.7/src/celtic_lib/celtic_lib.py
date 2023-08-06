import requests


class LTIValidatorException(Exception):
    def __init__(self, message, errors):
        super(LTIValidatorException, self).__init__(message)
        self.message = message[0]
        self.status_code = message[1]
        self.errors = errors


class DataRequester(object):
    def post(self, endpoint, data=None):
        """ Wrapper around requests.post """
        try:
            return requests.post(endpoint, json=data)
        except requests.RequestException as e:
            raise LTIValidatorException([str(e), 400], {})


class LTIValidator(object):

    def __init__(self, requester, endpoint_url, app_key):
        """
        @param requester -> A class instance will be handling the networking of
            the LTI validation request. 
                The requester MUST expose a post method which raises an LTIValidatorException on an unsuccessful request.
                The requester post method MUST return an object which has:
                    status_code property: The HTTP status code of the response
                    json() method: Returns the JSON of the response. Throws a ValueError if there is not JSON body
        @param endpoint_url -> string The URL of the server this class will be
            sending the data to
        @param app_key -> string A unique identifier this application uses to
            identify itself with the server
        """
        self._endpoint = endpoint_url
        self._app_key = app_key
        self._requester = requester

    def validate_request(self, launch_uri, http_method, payload):
        """
        Posts a validation request to the server, and returns the response.
        Would recommend the developer reading https://tools.ietf.org/html/rfc5849
            to familiarise themselves with OAuth1

        @param launch_uri -> string The URI this application was launched with
        @param http_method -> string "POST" | "GET" The HTTP method received on
            the LTI request
        @param payload -> dict A dictionary of LTI launch data parameters.
            https://www.imsglobal.org/specs/ltiv1p1/implementation-guide#toc-3
            details which parameters are required under the "Basic Launch Data"
            section.
        @return status_code -> int, result -> dict
            status_code is the HTTP status code of the request
            result is the server JSON response
        @raise LTIValidatorException if the json() method of self._requester.json() throws a ValueError
        @raise LTIValidatorException if the data requester has issues connecting to target
        @raise LTIValidatorException if the response code is not 200 or response.valid is not True
        """
        network_request = self._requester.post(self._endpoint, data={
            "appKey": self._app_key,
            "uri": launch_uri,
            "method": http_method,
            "payload": payload
        })

        status = network_request.status_code
        try:
            result = network_request.json()
        except ValueError as e:
            raise LTIValidatorException([str(e), 400], {})

        if status >= 400 or result.get("valid") is not True:
            result_message = result.get(
                "error", "Server has not provided an error message")
            raise LTIValidatorException((result_message, status), result)

        return status, result
