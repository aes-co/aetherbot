from core.database import get_database
import logging
from datetime import datetime
from typing import List, Dict

log = logging.getLogger(__name__)

class Case:
    COLLECTION_NAME = "cases"

    def __init__(self, case_id: str, title: str, created_by: int,
                 created_at: int = None, status: str = "open",
                 description: str = None, evidence_count: int = 0):
        self.case_id = case_id
        self.title = title
        self.created_by = created_by
        self.created_at = created_at if created_at is not None else int(datetime.now().timestamp())
        self.status = status
        self.description = description
        self.evidence_count = evidence_count

    def to_dict(self):
        return {
            "case_id": self.case_id,
            "title": self.title,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "status": self.status,
            "description": self.description,
            "evidence_count": self.evidence_count
        }

    @staticmethod
    async def get_case(case_id: str):
        db = get_database()
        case_data = await db[Case.COLLECTION_NAME].find_one({"case_id": case_id})
        if case_data:
            return Case(**case_data)
        return None

    @staticmethod
    async def get_cases_by_user(user_id: int):
        db = get_database()
        cursor = db[Case.COLLECTION_NAME].find({"created_by": user_id}).sort("created_at", -1)
        return [Case(**data) async for data in cursor]

    async def save(self):
        db = get_database()
        await db[Case.COLLECTION_NAME].update_one(
            {"case_id": self.case_id},
            {"$set": self.to_dict()},
            upsert=True
        )
        log.info(f"Case '{self.title}' ({self.case_id}) saved/updated in DB.")

    async def delete(self):
        db = get_database()
        await db[Case.COLLECTION_NAME].delete_one({"case_id": self.case_id})
        log.info(f"Case '{self.title}' ({self.case_id}) deleted from DB.")