import logging
from contextlib import asynccontextmanager
from typing import List, Annotated, AsyncIterator, Optional

from fastapi import FastAPI, Query, Header
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from starlette.responses import Response

from src.database_adapter import get_filtered_data, Filter, GroupByParameter
from src.utils import (
    ENDPOINT_RESPONSE_TYPE,
    ENPOINT_PARAMETER_ENTITIES_DESCRIPTION,
    ENPOINT_PARAMETER_YEARS_DESCRIPTION,
    parameter_to_list,
)

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """
    Configure FastAPI Caching
    :param _: Noop
    """
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
    yield


app = FastAPI(lifespan=lifespan)


@cache(expire=60)
@app.get(
    path="/measurements/",
    responses={**ENDPOINT_RESPONSE_TYPE},
)
@app.get(
    path="/measurements/{group_by}",
    responses={**ENDPOINT_RESPONSE_TYPE},
)
@cache(expire=60)
async def get_measurements(
    entities: str | None = Query(
        None,
        description=ENPOINT_PARAMETER_ENTITIES_DESCRIPTION
    ),
    years: str | None = Query(
        None,
        description=ENPOINT_PARAMETER_YEARS_DESCRIPTION
    ),
    accept: Annotated[str | None, Header()] = None,
    group_by: Optional[GroupByParameter | None] = None
):
    """
    Endpoint for fetching data, cached
    :param entities: The entities you want to query for
    :param years: The years you want to query for
    :param accept: Accept http header
    :param group_by: How the data will be grouped, either "Entity" or "Year"
    :return: json / csv
    """

    year_filters: List[int] | None = parameter_to_list(years, int)
    entity_filters: List[str] | None = parameter_to_list(entities, str)

    database_filter: Filter = {
        "Year": None,
        "Entity": None,
    }

    if years is not None:
        database_filter["Year"] = year_filters

    if entities is not None:
        database_filter["Entity"] = entity_filters

    result = get_filtered_data(filter=database_filter, group_by=group_by)

    if accept == "text/csv":
        return Response(
            content=result.to_csv(index=False),
            media_type="text/csv",
            headers={
                "Vary": "Accept",
                "Content-Disposition": "attachment; filename=data.csv",
            },
        )

    else:
        # Convert to dict so that FastApi can automatically convert to Json
        if group_by:
            group_by_str: str = group_by.title()
            return result.groupby(group_by_str).apply(
                lambda x: x.set_index(group_by_str).to_dict(orient="records")
            )

        return result.to_dict(orient="records")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app")
