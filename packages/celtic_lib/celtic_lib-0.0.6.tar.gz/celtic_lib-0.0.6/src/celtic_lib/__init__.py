from .celtic_lti import DataRequester, LTIValidator, LTIValidatorException


def get_lti_validator(endpoint_url, app_key):
    """
        Convenience method to inject the default DataRequester into the LTIValidator

        @param endpoint_url -> string The URL of the server this class will be 
            sending the data to
        @param app_key -> string A unique identifier this application uses to 
            identify itself with the server
        @return LTIValidator
    """
    return LTIValidator(DataRequester(), endpoint_url, app_key)
