from core.data.dao.line_dao import LineDAO
from core.data.models.employee_model import LineModel


class LineRepository:

    def __init__(self, dao: LineDAO):
        self.dao = dao

    async def get_lines(self) -> list[LineModel]:

        try:
            _respond = await self.dao.fetch_get_lines()

            if _respond:
                return [LineModel(**line.to_dict()) for line in _respond]

            return []
        except Exception as e:
            print(e)
            return []


