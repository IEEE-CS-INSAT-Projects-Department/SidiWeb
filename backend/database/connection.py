from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from core.config import settings
from typing import Optional

#Singleton MongoDB connection manager
#Manages a single connection pool to MongoDB with lazy initialization
class MongoDBManager:
    _client: Optional[AsyncIOMotorClient] = None
    _db: Optional[AsyncIOMotorDatabase] = None
    
    @classmethod
    def get_client(cls) -> AsyncIOMotorClient:
        """ Get or create MongoDB client with connection pooling
         Returns: AsyncIOMotorClient instance
        Note: Uses lazy initialization; connection is only established on first use"""
        
        if cls._client is None:
            cls._client = AsyncIOMotorClient(
                settings.mongodb_uri,
                maxPoolSize=10,
                minPoolSize=1,
            )
        return cls._client
    
    @classmethod
    def get_db(cls) -> AsyncIOMotorDatabase:
        
        # Get database instance from the connection pool.
        # Returns:AsyncIOMotorDatabase instance for the configured database

        if cls._db is None:
            client = cls.get_client()
            cls._db = client[settings.mongodb_db_name]
        return cls._db
    
    @classmethod
    async def close_connection(cls) -> None:
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None
    
    @classmethod
    async def ping(cls) -> bool:
        try:
            # Try to ping the database
            await cls.get_client().admin.command('ping')
            return True
        except Exception:
            return False


# Public interface functions
def get_db() -> AsyncIOMotorDatabase:
    return MongoDBManager.get_db()


async def close_db() -> None:
    await MongoDBManager.close_connection()


async def ping_db() -> bool:
    return await MongoDBManager.ping()

db = get_db()
