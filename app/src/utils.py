from typing import Callable, List, TypeVar
from starlette import status


T = TypeVar("T")


def parameter_to_list(
    parameter: str | None,
    return_type: Callable[[str], T]
) -> List[T] | None:
    """
    Convert a comma separated string to a list with given type
    :param parameter: The string to separate
    :param return_type: The type to return values in
    :return:
    """
    if parameter is None:
        return None

    temp = []
    if "," in parameter:
        temp = [return_type(p) for p in parameter.split(",")]
    else:
        temp.append(return_type(parameter))
    return temp


ENDPOINT_RESPONSE_TYPE = {
    status.HTTP_200_OK: {
        "content": {
            "application/json": {},
            "text/csv": {},
        }
    },
}

ENPOINT_PARAMETER_ENTITIES_DESCRIPTION = "The entities you want to query for. E.g. 'Germany' or 'Germany,China' (multiple entities have to be comma separated)"
ENPOINT_PARAMETER_YEARS_DESCRIPTION = "The years you want to query for. E.g. '2014' or '2014,2015' (multiple years have to be comma separated)"
