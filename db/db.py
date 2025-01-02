def insert_player(cur, logger, name, school, startTime, endTime, ip_address):
    cur.execute("INSERT INTO players (name, school, startTime, endTime, ip_address) VALUES (?, ?, ?, ?, ?)", (name, school, startTime, endTime, ip_address))
    logger.info(f"Player {name} inserted successfully!")

def get_players(cur, logger):
    logger.info("Players requested successfully!")
    return cur.execute("SELECT * FROM players").fetchall()

def check_player_ip(cur, logger, ip_address):
    count = cur.execute("SELECT COUNT(*) FROM players WHERE ip_address = ?", (ip_address,)).fetchone()[0]
    logger.info(f"IP check for {ip_address} returned {count} entries.")
    return count > 0
