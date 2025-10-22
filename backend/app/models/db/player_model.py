import psycopg2
from app.core.settings import supabase_connection_uri

# READ from Database
def get_player_by_name(player_name: str):
    """Retrieve a player by name."""
    try:
        conn = psycopg2.connect(supabase_connection_uri)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, player_name, photo_url 
            FROM players 
            WHERE player_name = %s;
            """,
            (player_name,)
        )
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print(f"[WARNING] Database connection failed: {e}")
        print("[INFO] Continuing without database cache...")
        return None

# WRITE to Database
def insert_player(player_id: int, player_name: str, photo_url: str):
    """Insert a player into the database (idempotent)."""
    try:
        conn = psycopg2.connect(supabase_connection_uri)
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO players (id, player_name, photo_url)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
            """,
            (player_id, player_name, photo_url)
        )
        conn.commit()
        cur.close()
        conn.close()
        print(f"[INFO] Player inserted: {player_name} ({player_id})")
    except Exception as e:
        print(f"[WARNING] Database connection failed: {e}")
        print("[INFO] Continuing without database cache...")

