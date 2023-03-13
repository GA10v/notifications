from pathlib import Path

from db.models.template import Template
from db.storage import PGStorage
from models.events import Event
from models.template import TemplateFromDB
from sqlalchemy import select


async def get_template(db: PGStorage, data: Event) -> TemplateFromDB:
    query = select(
        Template.subject,
        Template.template_files,
        Template.text_msg,
        Template.text_to_promo,
    ).filter(Template.event_type == data.event_type)
    result = await db.execute(query)

    if not result:
        return None

    (row,) = result
    _template = TemplateFromDB(**row)

    if not Path(f'{Path(__file__).parent.parent}/{_template.template_files}/message.html').is_file():
        raise ValueError('File not found')

    with open(f'{Path(__file__).parent.parent}/{_template.template_files}/message.html') as file:
        _template.template_files = file.read()
    return _template
