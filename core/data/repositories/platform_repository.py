from sqlalchemy.orm import Session

from core.data.dao.hbh_dao import PlatformDAO


class PlatformRepository:
    def __init__(self, db: Session):
        self.dao = PlatformDAO(db)

    async def get_platforms(self):

        try:
            _respond = await self.dao.fetch_get_platforms()

            if _respond:
                return _respond

            return []
        except Exception as e:
            print(e)
            return []
        finally:
            self.dao.session.remove()