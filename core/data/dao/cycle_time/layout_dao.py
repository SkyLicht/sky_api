from sqlalchemy.orm import joinedload

from core.data.schemas.all_schemas import LayoutSchema


# DAO implementation 3.0
class LayoutDAO:
    def __init__(self, session):
        self.session = session

    # For API call
    async def fetch_get_layout_by_id(self, layout_id):
        layout = self.session.query(LayoutSchema).filter_by(id=layout_id).first()
        return layout

    async def fetch_get_layouts(self):
        return self.session.query(LayoutSchema).all()

    async def fetch_get_layout_by_line_id(self, line_id)-> list[LayoutSchema]:
        layout = (
            self.session
            .query(LayoutSchema)
            .options(
                joinedload(LayoutSchema.station),
                joinedload(LayoutSchema.cluster),
                joinedload(LayoutSchema.line),
                joinedload(LayoutSchema.machine),
                joinedload(LayoutSchema.layout_section)
            )
            .filter_by(line_id=line_id).all())

        return layout

    # For Internal use

    # Static method to add a record to the database
