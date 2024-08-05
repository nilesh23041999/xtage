from django.http import JsonResponse


def response_structure(success, data, errorcode, errormessage, popupmessage, toast_type, toast_header, toast_body):
    """ 
        function returns the basic structure of the response class to be followed by every URL
    """
    return {
        "response": success,
        "data": data,
        "errorcode": errorcode,
        "errormessage": errormessage,
        "popupmessage": popupmessage,
        "type": toast_type,
        "header": toast_header,
        "body": toast_body
        }


class OkResponse(JsonResponse):
    def __init__(self, data="OK", popupmessage=False, toast_type="", toast_header="", toast_body=""):
        super(OkResponse, self).__init__(response_structure(True, data, None, None ,popupmessage, toast_type, toast_header, toast_body))


class ErrorResponse(JsonResponse):


    def __init__(self, error_code=None, error_message='', toast_type="error", toast_header="Error", toast_body='', 
                 additional_message='', context='', popupmessage=True, **kwargs):
        error_code = error_code if error_code is not None else getattr(self, 'error_code', None)
        error_message = error_message if error_message else getattr(self, 'error_message', '')
        toast_type = toast_type if toast_type else getattr(self, 'toast_type', "error")
        toast_header = toast_header if toast_header else getattr(self, 'toast_header', "Error")
        toast_body = toast_body if toast_body else getattr(self, 'toast_body', '')

        # Handle additional messages and context
        error_message += additional_message
        toast_body += context

        # Call super with constructed response data
        super().__init__(response_structure(
            False, None, error_code, error_message, 
            popupmessage, toast_type, 
            toast_header, toast_body
        ))

class MissingQueryParameterResponse(ErrorResponse):
    error_code = 400  # Bad Request
    error_message = "Query parameter 'q' is required"
    toast_type = "error"
    toast_header = "Bad Request"
    toast_body = "The query parameter 'q' is missing."

class RequestTimeOutErrorResponse(ErrorResponse):
    error_code = 408  # Request Timeout
    error_message = "The request timed out"
    toast_type = "error"
    toast_header = "Request Timeout"
    toast_body = "The request took too long to process."

class InternalServerErrorResponse(ErrorResponse):
    error_code = 500  # Internal Server Error
    error_message = "An internal server error occurred"
    toast_type = "error"
    toast_header = "Server Error"
    toast_body = "An unexpected error occurred. Please try again later."

class InvalidRequestInformation(ErrorResponse):
    error_code = 400  # Bad Request
    error_message = "Invalid request information"
    toast_type = "error"
    toast_header = "Bad Request"
    toast_body = "The request contains invalid or missing information. Please check your input and try again."

class AdditionalFieldProvidedResponse(ErrorResponse):
    error_code = 422  # Unprocessable Entity
    error_message = "Additional fields provided in the request"
    toast_type = "warning"
    toast_header = "Additional Fields"
    toast_body = "The request contains additional fields that are not expected. Please review the request parameters."

class SubmitRecommendationErrorResponse(ErrorResponse):
    error_code = 400  # Bad Request
    error_message = "Invalid recommendation submission"
    toast_type = "error"
    toast_header = "Submission Error"
    toast_body = "There was an error processing your recommendation. Please check your input."

class ListRecommendationsErrorResponse(ErrorResponse):
    error_code = 400  # Bad Request
    error_message = "Invalid filter parameters"
    toast_type = "error"
    toast_header = "Filter Error"
    toast_body = "There was an error with the filter parameters. Please adjust your search criteria."

class ManageUserInteractionsErrorResponse(ErrorResponse):
    error_code = 400  # Bad Request
    error_message = "Invalid user interaction data"
    toast_type = "error"
    toast_header = "Interaction Error"
    toast_body = "There was an error processing your interaction. Please check your input."
