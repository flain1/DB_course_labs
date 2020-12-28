from sqlalchemy import DDL
from sqlalchemy import event


class TrgmExtension:
    @classmethod
    def add_create_trgm_extension_trigger(cls):
        """Call this for any tables that use trgm indexes to ensure they have the pg_trgm extension already available."""
        trigger = DDL('CREATE EXTENSION IF NOT EXISTS "pg_trgm";')
        event.listen(
            cls.__table__, "before_create", trigger.execute_if(dialect="postgresql")
        )
