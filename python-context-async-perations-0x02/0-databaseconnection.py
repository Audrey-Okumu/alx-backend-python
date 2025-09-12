import sqlite3


class DatabaseConnection:
    """Context manager for SQLite database connection"""

    def __init__(self, db_name):
        """Initialize with database file name"""
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """Open the connection and return a cursor"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """Commit changes (if any) and close the connection"""
        if self.conn:
            if exc_type is None:  # no exception
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()
