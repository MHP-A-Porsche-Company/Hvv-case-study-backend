import logging
from contextlib import asynccontextmanager
from typing import List, Annotated, AsyncIterator, TypeVar

from fastapi import FastAPI, Query, Header
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from starlette import status
from starlette.responses import Response

from src.database_adapter import get_filtered_data, Filter

log = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """
    Configure FastAPI Caching
    :param _: Noop
    """
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
    yield

app = FastAPI(lifespan = lifespan)

T = TypeVar("T")

def parameter_to_list(parameter: str, return_type: T) -> List[T] | None:
    """
    Convert a comma separated string to a list with given type
    :param parameter: The string to separate
    :param return_type: The type to return values in
    :return:
    """
    if parameter is not None:
        temp = []
        if "," in parameter:
            temp = [return_type(p) for p in parameter.split(",")]
        else:
            temp.append(return_type(parameter))
        return temp
    return None

@cache(expire = 60)
@app.get(
    path = "/measurements/",
    responses = {
        status.HTTP_200_OK: {
            "content": {
                "application/json": {},
                "text/csv": {},
            }
        },
    },
)
@cache(expire = 60)
def get_measurements(
    entities: str | None = Query(None, description = "The entities you want to query for. E.g. 'Germany' or 'Germany,China' (multiple entities have to be comma separated)"),
    years: str | None = Query(None, description = "The years you want to query for. E.g. '2014' or '2014,2015' (multiple years have to be comma separated)"),
    accept: Annotated[str | None, Header()] = None,
):
    """
        Endpoint for fetching data, cached
        :param entities: The entities you want to query for
        :param years: The years you want to query for
        :param accept: Accept http header
        :return: json / csv
    """

    year_filters: List[int] | None = parameter_to_list(years, int)
    entity_filters: List[str] | None =  parameter_to_list(entities, str)

    database_filter: Filter = {}

    if years is not None:
        database_filter["Year"] = year_filters

    if entities is not None:
        database_filter["Entity"] = entity_filters

    result = get_filtered_data(filter = database_filter)

    if accept == "text/csv":
        return Response(
            content = result.to_csv(index = False),
            media_type = "text/csv",
            headers = {
                "Vary": "Accept",
                "Content-Disposition": "attachment; filename=data.csv",
            }
        )

    else:
        # Convert to dict so that FastApi can automatically convert to Json
        return result.to_dict(orient = "records")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app")