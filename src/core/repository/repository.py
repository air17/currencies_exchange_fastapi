from sqlalchemy.ext.asyncio import AsyncSession


class Repository:
    """Base repository class"""

    def __init__(self, db: AsyncSession):
        """Initialize the repository with the database session."""
        self.db: AsyncSession = db
