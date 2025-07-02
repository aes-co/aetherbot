from core.database import get_database
import logging
from datetime import datetime
from typing import Dict

log = logging.getLogger(__name__)

class Evidence:
    COLLECTION_NAME = "evidence"

    def __init__(self, evidence_id: str, case_id: str, type: str, content: str,
                 added_by: int, added_at: int = None, description: str = None,
                 metadata: Dict = None):
        self.evidence_id = evidence_id
        self.case_id = case_id
        self.type = type # e.g., "text", "link", "photo", "document", "user_info"
        self.content = content
        self.added_by = added_by
        self.added_at = added_at if added_at is not None else int(datetime.now().timestamp())
        self.description = description
        self.metadata = metadata if metadata is not None else {}

    def to_dict(self):
        return {
            "evidence_id": self.evidence_id,
            "case_id": self.case_id,
            "type": self.type,
            "content": self.content,
            "added_by": self.added_by,
            "added_at": self.added_at,
            "description": self.description,
            "metadata": self.metadata
        }

    @staticmethod
    async def get_evidence(evidence_id: str):
        db = get_database()
        evidence_data = await db[Evidence.COLLECTION_NAME].find_one({"evidence_id": evidence_id})
        if evidence_data:
            return Evidence(**evidence_data)
        return None

    @staticmethod
    async def get_evidence_by_case(case_id: str):
        db = get_database()
        cursor = db[Evidence.COLLECTION_NAME].find({"case_id": case_id}).sort("added_at", 1)
        return [Evidence(**data) async for data in cursor]

    async def save(self):
        db = get_database()
        await db[Evidence.COLLECTION_NAME].update_one(
            {"evidence_id": self.evidence_id},
            {"$set": self.to_dict()},
            upsert=True
        )
        log.info(f"Evidence '{self.evidence_id}' added to case '{self.case_id}'.")

    async def delete(self):
        db = get_database()
        await db[Evidence.COLLECTION_NAME].delete_one({"evidence_id": self.evidence_id})
        log.info(f"Evidence '{self.evidence_id}' deleted.")