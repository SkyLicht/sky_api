# DAO implementation 3.0
from core.data.schemas.all_schemas import LineSchema


class LineDAO:

    def __init__(self, session):
        self.session = session

    async def fetch_get_lines(self)-> list[LineSchema]:
        return self.session.query(LineSchema).all()

    async def fetch_get_line(self, line_id) -> LineSchema | None:
        line = self.session.query(LineSchema).filter_by(id=line_id).first()
        return line
    async def fetch_get_line_by_name(self, line_name) -> LineSchema | None:
        line = self.session.query(LineSchema).filter_by(name=line_name).first()
        return line