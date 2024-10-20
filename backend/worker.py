import models
from celery import Celery
from database import get_session
from sqids import Sqids

sqids = Sqids()
celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)

celery_app.conf.update(
    result_expires=3600,
)


@celery_app.task()
def shrink_url(input_url: str):  # noqa: ANN201
    # turn URL into list of ASCII values
    url_in_asci = [ord(c) for c in input_url]
    # Shrink using Sqids
    short_url = sqids.encode(url_in_asci)

    db_obj = models.UrlMapping(
        original_url=input_url,
        short_url=short_url,
    )
    session_generator = get_session()
    session = next(session_generator)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
