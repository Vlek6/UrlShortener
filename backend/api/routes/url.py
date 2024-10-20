from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse

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
    input_url = input_form.original_url.strip()

    if input_url.startswith("http://"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="http URLs are not handled",
        )
    if not input_url.startswith("https://"):
        input_url = "https://" + input_url

    # Try to obtain existing short version of that URL
    db_url = url.get_db_url_with_long_url(session=session, url=input_url)
    # Check if URL already exists in database
    if db_url:
        return db_url

    db_obj = models.UrlMapping(
        original_url=input_url,
        short_url=url.shrink_url(input_url=input_url),
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)

    return db_obj


@router.get("/{shortened}")
def redirect_to_original_url(*, session: SessionDep, shortened: str):  # noqa: ANN201
    db_obj = url.get_db_url_with_short_url(session=session, url=shortened)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shortened URL not found",
        )
    return RedirectResponse(url=db_obj.original_url)
