from .response_handler import *

def request_handler(request, compulsory_query_parameters=None, optional_query_parameters=None, optional_body_args=None, **kwargs):
    """
    Handle and validate request parameters including compulsory and optional query parameters and body arguments.

    Args:
        request (HttpRequest): The request object.
        compulsory_query_parameters (list): List of compulsory query parameters.
        optional_query_parameters (list): List of optional query parameters.
        optional_body_args (list): List of optional body arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        dict: A dictionary containing extracted query parameters and body parameters.
    """
    if compulsory_query_parameters is None:
        compulsory_query_parameters = []
    if optional_query_parameters is None:
        optional_query_parameters = []
    if optional_body_args is None:
        optional_body_args = []

    # Extract query parameters
    query_params = request.query_params
    missing_query_params = [param for param in compulsory_query_parameters if param not in query_params]

    if missing_query_params:
        return InvalidRequestInformation(
            error_message="Missing compulsory query parameters",
            toast_body=f"Missing parameters: {', '.join(missing_query_params)}"
        )

    # Extract body parameters
    body_params = request.data
    missing_body_args = [arg for arg in optional_body_args if arg not in body_params]
    
    if missing_body_args:
        return InvalidRequestInformation(
            error_message="Missing body parameters",
            toast_body=f"Missing parameters: {', '.join(missing_body_args)}"
        )

    expected_params = compulsory_query_parameters + optional_query_parameters + optional_body_args
    all_params = list(query_params.keys()) + list(body_params.keys())
    additional_params = [param for param in all_params if param not in expected_params]

    if additional_params:
        return AdditionalFieldProvidedResponse(
            error_code=233,
            error_message=f"Additional arguments {additional_params} provided!"
        )

    # Extract and return parameters
    extracted_query_params = {param: query_params.get(param) for param in compulsory_query_parameters + optional_query_parameters}
    extracted_body_params = {arg: body_params.get(arg) for arg in optional_body_args}
    
    return {
        'query_params': extracted_query_params,
        'body_params': extracted_body_params
    }
