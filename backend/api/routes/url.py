from fastapi import APIRouter, status

from backend import models
from backend.api.deps import SessionDep
from backend.crud import url

router = APIRouter()


@router.post(
    "/shrink",
    response_model=models.UrlMappingPublic,
    status_code=status.HTTP_302_FOUND,
)
def shrink_url(
    *,
    session: SessionDep,
    input_form: models.UrlMappingForm,
) -> models.UrlMappingPublic:
    # Try to obtain existing short version of that URL
    db_url = url.get_db_url(session=session, url=input_form.original_url)
    # Check if URL already exists in database
    if db_url:
        return db_url

    db_obj = models.UrlMapping(
        original_url=input_form.original_url,
        short_url=url.shrink_url(input_url=input_form.original_url),
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)

    return db_obj
