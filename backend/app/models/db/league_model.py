import psycopg2
from app.core.settings import supabase_connection_uri

# Write to Database
def get_league_by_name(league_name: str):
    conn = psycopg2.connect(supabase_connection_uri)
    cur = conn.cursor()
    cur.execute("SELECT id, league_name FROM leagues WHERE league_name = %s;", (league_name,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result

# Read from Database
def insert_league(league_id: int, league_name: str):
    conn = psycopg2.connect(supabase_connection_uri)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO leagues (id, league_name)
        VALUES (%s, %s)
        ON CONFLICT (id) DO NOTHING;
        """,
        (league_id, league_name),
    )
    conn.commit()
    cur.close()
    conn.close()