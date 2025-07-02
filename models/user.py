from core.database import get_database
import logging
from datetime import datetime

log = logging.getLogger(__name__)

class User:
    COLLECTION_NAME = "users"

    def __init__(self, user_id: int, username: str = None, first_name: str = None,
                 is_admin: bool = False, registered_at: int = None):
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.is_admin = is_admin
        self.registered_at = registered_at if registered_at is not None else int(datetime.now().timestamp())

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "first_name": self.first_name,
            "is_admin": self.is_admin,
            "registered_at": self.registered_at
        }

    @staticmethod
    async def get_user(user_id: int):
        db = get_database()
        user_data = await db[User.COLLECTION_NAME].find_one({"user_id": user_id})
        if user_data:
            return User(**user_data)
        return None

    async def save(self):
        db = get_database()
        await db[User.COLLECTION_NAME].update_one(
            {"user_id": self.user_id},
            {"$set": self.to_dict()},
            upsert=True
        )
        log.info(f"User {self.user_id} saved/updated in DB.")

    async def update_admin_status(self, status: bool):
        db = get_database()
        await db[User.COLLECTION_NAME].update_one(
            {"user_id": self.user_id},
            {"$set": {"is_admin": status}}
        )
        self.is_admin = status
        log.info(f"User {self.user_id} admin status updated to {status}.")