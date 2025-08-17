"""
MechanicalMind Compatibility Matrix v2.0
Package version compatibility database manager
"""

import sqlite3
from typing import Dict, List
from pathlib import Path


class CompatibilityMatrix:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or str(
            Path(__file__).parent / "knowledge_base" / "version_compatibility.db"
        )
        self._init_db()

    def _init_db(self):
        """Initialize database schema if not exists"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS package_versions (
                    package TEXT NOT NULL,
                    version TEXT NOT NULL,
                    python_version TEXT NOT NULL,
                    status TEXT CHECK(status IN ('compatible', 'incompatible', 'untested')),
                    PRIMARY KEY (package, version, python_version)
                )
            """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS package_relations (
                    parent_package TEXT NOT NULL,
                    parent_version TEXT NOT NULL,
                    child_package TEXT NOT NULL,
                    child_version_range TEXT NOT NULL,
                    relation_type TEXT CHECK(relation_type IN ('depends', 'conflicts')),
                    PRIMARY KEY (parent_package, parent_version, child_package)
                )
            """
            )
            conn.commit()

    def add_compatibility_record(
        self, package: str, version: str, python_version: str, status: str
    ) -> bool:
        """Add or update compatibility record"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO package_versions VALUES (?, ?, ?, ?)",
                    (package, version, python_version, status),
                )
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def check_compatibility(
        self, package: str, version: str, python_version: str
    ) -> str:
        """Check compatibility status for a package version"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT status FROM package_versions
                WHERE package = ? AND version = ? AND python_version = ?
            """,
                (package, version, python_version),
            )

            result = cursor.fetchone()
            return result[0] if result else "untested"

    def find_compatible_versions(self, package: str, python_version: str) -> List[str]:
        """Get all compatible versions for a package"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT version FROM package_versions
                WHERE package = ? AND python_version = ? AND status = 'compatible'
                ORDER BY version DESC
            """,
                (package, python_version),
            )

            return [row[0] for row in cursor.fetchall()]

    # [...] (Additional methods for relationship management)
