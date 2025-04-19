import sqlite3
from pathlib import Path


class CompatibilityMatrix:
    def __init__(self, db_path: str = "knowledge_base/version_compatibility.db"):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        """Create database tables if they don't exist"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS package_versions (
                    package TEXT NOT NULL,
                    version TEXT NOT NULL,
                    python_version TEXT NOT NULL,
                    status TEXT NOT NULL,
                    PRIMARY KEY (package, version, python_version)
                )
            """
            )
            conn.commit()

    def _validate_input(
        self, package: str, version: str, python_version: str, status: str
    ) -> bool:
        """Validate input parameters"""
        if not all([package, version, python_version, status]):
            return False
        return True

    def add_compatibility_record(
        self, package: str, version: str, python_version: str, status: str
    ) -> bool:
        """Add or update compatibility record"""
        if not self._validate_input(package, version, python_version, status):
            return False

        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO package_versions VALUES (?, ?, ?, ?)",
                    (package, version, python_version, status),
                )
                conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def check_compatibility(
        self, package: str, version: str, python_version: str
    ) -> str:
        """Check package compatibility status"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT status FROM package_versions WHERE package=? AND version=? AND python_version=?",
                (package, version, python_version),
            )
            result = cursor.fetchone()
            return result[0] if result else "unknown"
