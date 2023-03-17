# type: ignore
from typing import Any

from jinja2 import BaseLoader, Environment, Template

from models.payloads import payload
from models.template import TemplateFromDB
from service.render.protocol import RenderProtocol


class JiniaRender(RenderProtocol):
    async def render(self, template: TemplateFromDB, data: payload, **kwargs: dict[Any, Any]) -> str:
        _template: Template = Environment(
            loader=BaseLoader,
            enable_async=True,
        ).from_string(template.template_files)
        return str(await _template.render_async(**data.dict()))
