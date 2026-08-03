import sqlite3
from datetime import datetime

from runtime.state import RuntimeState

RUNTIME_ID = "runtime"
class RuntimeStateStore:

    def __init__(self, db_path="state_store.db"):

        self.conn = sqlite3.connect(
            db_path,
            check_same_thread=False
        )

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS runtime_state(
            id TEXT PRIMARY KEY,
            memory_count INTEGER,
            last_reflection_time TEXT,
            memory_count_after_reflection INTEGER,
            reflection_count INTEGER,
            last_lifecycle_run_time TEXT
        )
        """)
        columns = {
            row[1]
            for row in self.conn.execute("PRAGMA table_info(runtime_state)")
        }
        if "last_lifecycle_run_time" not in columns:
            self.conn.execute(
                "ALTER TABLE runtime_state ADD COLUMN last_lifecycle_run_time TEXT"
            )
        self.conn.commit()

    def load(self) -> RuntimeState:
        cursor = self.conn.execute(
            """
            SELECT memory_count, last_reflection_time,
                   memory_count_after_reflection, reflection_count,
                   last_lifecycle_run_time
            FROM runtime_state
            WHERE id = ?
            """,
            (RUNTIME_ID,),
        )

        row = cursor.fetchone()

        if row is None:
            return RuntimeState()

        return RuntimeState(
            memory_count=row[0],
            last_reflection_time=(
                datetime.fromisoformat(row[1])
                if row[1] is not None
                else None
            ),
            memory_count_after_reflection=row[2],
            reflection_count=row[3],
            last_lifecycle_run_time=(
                datetime.fromisoformat(row[4])
                if row[4] is not None
                else None
            ),
        )

    def save(self,state : RuntimeState):
        self.conn.execute(
            """
            INSERT OR REPLACE
            INTO runtime_state(
                id, memory_count, last_reflection_time,
                memory_count_after_reflection, reflection_count,
                last_lifecycle_run_time
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                RUNTIME_ID,
                state.memory_count,
                state.last_reflection_time.isoformat()
                if state.last_reflection_time
                else None,
                state.memory_count_after_reflection,
                state.reflection_count,
                state.last_lifecycle_run_time.isoformat()
                if state.last_lifecycle_run_time
                else None,
            )
        )

        self.conn.commit()

    def close(self):
        self.conn.close()
