# database.py

import ssl
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from db.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

Base = declarative_base()

# Используйте URL БЕЗ параметров запроса ssl
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Создайте пустой SSLContext, который не будет проверять сертификаты
# Это ОПАСНО для продакшена, но полезно для локальной отладки/самоподписанных сертификатов
# Если ваша БД требует валидный SSL, этот код не сработает
context = ssl.SSLContext()
context.verify_mode = ssl.CERT_NONE
context.check_hostname = False

engine = create_async_engine(
    DATABASE_URL,
    # Передайте этот контекст через connect_args
    connect_args={},
    # 🚀 КЛЮЧЕВЫЕ настройки
    pool_size=5,
    max_overflow=5,
    pool_timeout=15,
    pool_recycle=300,
    pool_pre_ping=True,
)

# ... (остальной код database.py остается прежним) ...


AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for FastAPI to get an async session."""
    async with AsyncSessionLocal() as session:
        yield session

