from schemas import TravelPlan,Traveler, Weather, VacationInfo, Activity, ActivityRecommendation, ItineraryDay
from pydantic import BaseModel
from helper import do_chat_completion
MODEL = "gpt-4.1-mini"

class AgentError(Exception):
    pass


class EvaluationResults(BaseModel):
    success: bool
    failures: list[str]
    eval_functions: list[str]

from helper import print_in_box

def get_eval_results(vacation_info, final_output, eval_functions) -> EvaluationResults:
    """
    Evaluates the final output of the itinerary agent against a set of evaluation functions.
    Args:
        vacation_info (VacationInfo): The vacation information used to generate the itinerary.
        final_output (TravelPlan): The final output from the itinerary agent.
        eval_functions (list[callable]): A list of evaluation functions to apply.
    Returns:
        EvaluationResults: An object containing the success status, any failures, and the names of the evaluation functions used.
    """
    if not isinstance(vacation_info, VacationInfo):
        raise ValueError("vacation_info must be an instance of VacationInfo")
    if not isinstance(final_output, TravelPlan):
        raise ValueError("final_output must be an instance of TravelPlan")
    if not isinstance(eval_functions, list) or not all(
        callable(fn) for fn in eval_functions
    ):
        raise ValueError("eval_functions must be a list of callable functions")
    eval_results = []
    for eval_fn in eval_functions:
        try:
            eval_fn(vacation_info, final_output)
        except AgentError as e:
            error_msg = str(e)
            print_in_box(error_msg, title="Evaluation Error")
            print("\n\n")

            eval_results.append(error_msg)
    return EvaluationResults(
        success=len(eval_results) == 0,
        failures=eval_results,
        eval_functions=[fn.__name__ for fn in eval_functions],
    )

def eval_start_end_dates_match(vacation_info: VacationInfo, final_output: TravelPlan):
    """Verifies that the arrival and departure dates in vacation_info match the start and end dates in final_output.

    Args:
        vacation_info (dict): Contains the vacation details including arrival and departure dates
        final_output (dict): Contains the itinerary details including start and end dates

    Raises:
        AgentError: If either the arrival date doesn't match the start date or the departure date doesn't match the end date
    """
    if (
        vacation_info.date_of_arrival != final_output.start_date
        or vacation_info.date_of_departure != final_output.end_date
    ):
        raise AgentError(
            f"Dates do not match: {vacation_info.date_of_arrival} != {final_output.start_date} or {vacation_info.date_of_departure} != {final_output.end_date}"
        )

    if final_output.start_date > final_output.end_date:
        raise AgentError(
            f"Start date is after end date: {final_output.start_date} > {final_output.end_date}"
        )


    


            if "IS_COMPATIBLE" in (resp or ""):
                is_compatible = True
            elif "IS_INCOMPATIBLE" in (resp or ""):
                is_compatible = False
            else:
                raise RuntimeError(
                    f"Unexpected response from the model: {resp}. Expected 'IS_COMPATIBLE' or 'IS_INCOMPATIBLE'."
                )

            if is_compatible:
                print(
                    f"✅ Activity {activity_recommendation.activity.name} (on {itinerary_day.date}) and weather '{weather_condition}' are compatible."
                )

            else:
                activities_that_are_incompatible.append(
                    activity_recommendation.activity.name
                )
                print(
                    f"❌ Activity {activity_recommendation.activity.name} (on {itinerary_day.date}) and weather '{weather_condition}' are incompatible."
                )

    if activities_that_are_incompatible:
        raise AgentError(
            f"Activities that may be ruined by inclement weather: {activities_that_are_incompatible}"
        )

def eval_itinerary_satisfies_interests(
    vacation_info: VacationInfo, final_output: TravelPlan
):
    """Verifies that the itinerary includes activities matching each traveler's interests.

    This function checks that each traveler has at least one activity in the itinerary that matches their interests.

        Args:
        vacation_info (dict): Contains the vacation details including traveler information and their interests
        final_output (dict): Contains the itinerary details including daily activities

    Raises:
        AgentError: If any traveler has no matching activities or if one traveler has more than twice
                   the number of matching activities compared to another traveler
    """
    traveler_to_interests = {}
    traveler_to_interest_hit_counts = {}

    for traveler in vacation_info.travelers:
        traveler_to_interests[traveler.name] = traveler.interests
        traveler_to_interest_hit_counts[traveler.name] = 0

    for traveler_name, interests in traveler_to_interests.items():
        for itinerary_day in final_output.itinerary_days:
            for activity_recommendation in itinerary_day.activity_recommendations:
                # Check if the activity matches any of the traveler's interests
                matching_interests = set(traveler_to_interests[traveler_name]) & set(
                    activity_recommendation.activity.related_interests
                )

                if matching_interests:
                    traveler_to_interest_hit_counts[traveler_name] += 1
                    print(
                        f"✅ Traveler {traveler_name} has a match with interest {matching_interests} at {activity_recommendation.activity.name}"
                    )

    travelers_with_no_interest_hits = [
        traveler
        for traveler, interest_hit_count in traveler_to_interest_hit_counts.items()
        if interest_hit_count == 0
    ]

    # If any of the travelers have 0 matches, raise an error
    if travelers_with_no_interest_hits:
        raise AgentError(
            f"Travelers {travelers_with_no_interest_hits} has no matches with the itinerary."
        )