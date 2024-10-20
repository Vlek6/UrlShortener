from datetime import datetime, timezone

import models  # noqa: TCH002
from api.deps import SessionDep  # noqa: TCH002
from crud import url
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse
from worker import shrink_url

router = APIRouter()


@router.post(
    "/shrink",
    status_code=status.HTTP_200_OK,
)
async def shrink_long_url(  # noqa: ANN201
    *,
    session: SessionDep,
    input_form: models.UrlMappingForm,
):
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

    shrink_url.delay(input_url)
    return JSONResponse(
        content={"message": "Your URL is being processed, check again in a while"},
    )


@router.get("/{shortened}")
def redirect_to_original_url(*, session: SessionDep, shortened: str):  # noqa: ANN201
    db_obj = url.get_db_url_with_short_url(session=session, url=shortened)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shortened URL not found",
        )
    db_obj.last_access = datetime.now(tz=timezone.utc)
    db_obj.click_count = db_obj.click_count + 1
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return RedirectResponse(url=db_obj.original_url)
