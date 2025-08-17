def get_tool_descriptions_string(fns):
    """Generates a tool description from a function's docstring.
    Args:
        fns (list): List of functions to generate descriptions for.
    Returns:
        str: A formatted string containing the function names and their descriptions."""
    resp = ""
    for fn in fns:
        function_name = fn.__name__
        function_doc = fn.__doc__ or "No description provided."

        resp += f"* `{function_name}`: {function_doc}\n"

    return resp

def calculator_tool(input_expression) -> float:
    """Evaluates a mathematical expression and returns the result as a float.

    Args:
        input_expression (str): A string containing a valid mathematical expression to evaluate.

    Returns:
        float: The result of the evaluated expression.

    Example:
        >>> calculator_tool("1 + 1")
        2.0
    """
    import numexpr as ne
    return float(ne.evaluate(input_expression))

def get_activities_by_date_tool(date: str, city: str) -> List[dict]:
    """
    Args: 
      date (str): the date to retreive the activity for
      city (str): the name of the city to search for activities
    Returns:
      List[dict]: list of activities that is compatible with the date and the city
    """
    from project_lib import call_activities_api_mocked
    resp = call_activities_api_mocked(date=date, city=city)

    return [Activity.model_validate(activity).model_dump() for activity in resp]

def final_answer_tool(final_output: TravelPlan) -> TravelPlan:
    """Returns the final travel plan

    Args:
        final_output (TravelPlan): The final travel plan to return.

    Returns:
        TravelPlan: The final travel plan.
    """
    return final_output