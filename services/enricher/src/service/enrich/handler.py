from models.base import EventType
from models.events import Event
from models.payloads import payload
from service.enrich.new_content import NewContentPayloads
from service.enrich.new_review_likes import NewReviewLikesPayloads
from service.enrich.new_user import NewUserPayload


async def get_payload(data: Event) -> payload:
    if data.event_type == EventType.welcome:
        payload = NewUserPayload(data)
    elif data.event_type == EventType.new_content:
        payload = NewContentPayloads(data)
    elif data.event_type == EventType.new_likes:  # noqa: E800
        payload = NewReviewLikesPayloads(data)
    # elif data.event_type == EventType.promo:  # noqa: E800
    #     ...

    return await payload.payload()
