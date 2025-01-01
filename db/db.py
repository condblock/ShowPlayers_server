def insert_player(cur, logger, name, school, startTime):
    cur.execute(f"INSERT INTO players (name, school, startTime) \
                  VALUES ('{name}', '{school}', '{startTime}')")
    logger.info(f"Player {name} inserted successfully!")

def get_players(cur, logger):
    logger.info(f"Players requested successfully!")
    return cur.execute("SELECT * FROM players").fetchall()