from core.data.dao.cycle_time.layout_dao import LayoutDAO


class LayoutRepository:
    def __init__(self, dao: LayoutDAO):
        self.dao = dao


    async def get_layouts(self):

        try:
            _respond = await self.dao.fetch_get_layouts()

            if _respond:
                return _respond

            return []
        except Exception as e:
            print(e)
            return []

    async def get_layout_by_id(self, layout_id):
        try:
            _respond = await self.dao.fetch_get_layout_by_id(layout_id)

            if _respond:
                return _respond

            return None
        except Exception as e:
            print(e)
            return None



    async def get_layout_by_line_id(self, line_id):
        try:
            _respond = await self.dao.fetch_get_layout_by_line_id(line_id)

            if _respond:
                return _respond

            return None
        except Exception as e:
            print(e)
            return None
