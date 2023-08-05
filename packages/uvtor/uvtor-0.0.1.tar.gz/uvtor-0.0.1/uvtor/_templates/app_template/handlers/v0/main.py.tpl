from apps.{appname}.handlers import BaseHandler
from uvtor.core.decorators.api import standard_api


class ExampleHandler(BaseHandler):

    @standard_api
    async def get(self):

        return {{
            'data': 'example'
        }}
