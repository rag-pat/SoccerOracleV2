import psycopg2
from app.core.settings import supabase_connection_uri

# Read from Database
def get_team_by_name(team_name: str, league_id: int):
    try:
        conn = psycopg2.connect(supabase_connection_uri)
        cur = conn.cursor()
        cur.execute("SELECT id, team_name FROM teams WHERE team_name = %s AND league_id = %s;", (team_name, league_id))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print(f"[WARNING] Database connection failed: {e}")
        print("[INFO] Continuing without database cache...")
        return None

# Write to Database
def insert_team(team_id: int, team_name: str, league_id: int):
    try:
        conn = psycopg2.connect(supabase_connection_uri)
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO teams (id, team_name, league_id)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
            """,
            (team_id, team_name, league_id),
        )
        conn.commit()
        print("[DEBUG] Commit successful for team:", team_name)
        cur.close()
        conn.close()
        print(f"[INFO] Cached team {team_name} (ID: {team_id}) to database")
    except Exception as e:
        print(f"[WARNING] Database connection failed: {e}")
        print("[INFO] Continuing without database cache...")