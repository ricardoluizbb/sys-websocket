import asyncpg
import os

async def init_db():
    conn = await asyncpg.connect(
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        database=os.getenv("POSTGRES_DB"),
        host='db'
    )
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS connected_users (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(255) UNIQUE NOT NULL,
            connected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    await conn.close()

async def add_user(user_id):
    conn = await asyncpg.connect(
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        database=os.getenv("POSTGRES_DB"),
        host='db'
    )
    await conn.execute('''
        INSERT INTO connected_users(user_id) VALUES($1)
        ON CONFLICT (user_id) DO NOTHING
    ''', user_id)
    await conn.close()

async def remove_user(user_id):
    conn = await asyncpg.connect(
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        database=os.getenv("POSTGRES_DB"),
        host='db'
    )
    await conn.execute('''
        DELETE FROM connected_users WHERE user_id = $1
    ''', user_id)
    await conn.close()
