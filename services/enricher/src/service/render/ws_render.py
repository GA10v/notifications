from models.payloads import NewContentContext, NewPromoContext, NewReviewsLikesContext, NewUserContext, payload
from models.template import TemplateFromDB
from service.render.protocol import RenderProtocol


class TextRender(RenderProtocol):
    async def render(self, template: TemplateFromDB, data: payload, **kwargs) -> str:
        if data is NewUserContext:
            return None
        elif data is NewReviewsLikesContext:
            return (
                template.text_msg.replace('{{user_name}}', data.user_name)
                .replace('{{movie_title}}', data.movie_title)
                .replace('{{likes}}', data.likes),
            )
        elif data is NewContentContext:
            return (
                template.text_msg.replace('{{user_name}}', data.user_name).replace('{{movie_title}}', data.movie_title),
            )
        elif data is NewPromoContext:
            return (
                template.text_msg.replace('{{user_name}}', data.user_name).replace(
                    '{{text_to_promo}}',
                    data.text_to_promo,
                ),
            )
