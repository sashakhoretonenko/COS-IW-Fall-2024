'''
Creates sqlite3 database to store all of Tang's games
'''

import sqlite3
import os
import chess.pgn
from io import StringIO
import numpy as np
#-----------------------------------------------------------------------

'''
Creates database
'''
def create_db(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Add necessary columns to table
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT,
            site TEXT,
            date TEXT,
            round TEXT,
            white TEXT,
            black TEXT,
            result TEXT,
            match TEXT,
            current_position TEXT,
            timezone TEXT,
            eco TEXT,
            eco_url TEXT,
            utc_date TEXT,
            utc_time TEXT,
            white_elo INTEGER,
            black_elo INTEGER,
            time_control TEXT,
            termination TEXT,
            start_time TEXT,
            end_time TEXT,
            link TEXT,
            moves TEXT)
            '''
        )
        conn.commit()
        return conn

    except sqlite3.Error as e:
         print(f"Error while creating database: {e}")
         return None
#-----------------------------------------------------------------------

'''
Inserts game into database
'''
def insert_game(cursor, headers):
    # Uses cursor to insert game
    cursor.execute(
        '''
        INSERT INTO games (
        event,
        site,
        date,
        round,
        white,
        black,
        result,
        match,
        current_position,
        timezone, 
        eco,
        eco_url,
        utc_date,
        utc_time,
        white_elo,
        black_elo,
        time_control, 
        termination,
        start_time,
        end_time,
        link,
        moves
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        (
            headers.get("Event", ""),
            headers.get("Site", ""),
            headers.get("Date", ""),
            headers.get("Round", ""),
            headers.get("White", ""),
            headers.get("Black", ""),
            headers.get("Result", ""),
            headers.get("Match", ""),
            headers.get("CurrentPosition", ""),
            headers.get("Timezone", ""),
            headers.get("ECO", ""),
            headers.get("ECOUrl", ""),
            headers.get("UTCDate", ""),
            headers.get("UTCTime", ""),
            headers.get("WhiteElo", ""),
            headers.get("BlackElo", ""),
            headers.get("TimeControl", ""),
            headers.get("Termination", ""),
            headers.get("StartTime", ""),
            headers.get("EndDate", ""),
            headers.get("Link", ""),
            headers.get("Moves", ""))
    )
    
#-----------------------------------------------------------------------

def parse_pgn(pgn_folder, conn):
    cursor = conn.cursor()

    for year in range(2014, 2025):
        year_folder = os.path.join(pgn_folder, f"{year} Games")

        for month in range(1, 13):
            month_file = f"penguingm1_{year}_{month:02d}.pgn"
            file_path = os.path.join(year_folder, month_file)
        
            # If statement is necessary because data only goes up to September 2024
            if os.path.exists(file_path):
                print(f"Processing {month}, {year}\n")  
                
                insert_file(file_path, cursor, conn)
#-----------------------------------------------------------------------
'''
Formats the necessary information from 
'''
def insert_file(file_path, cursor, conn):
    with open(file_path, 'r') as pgn_file:
        # headers that will be passed into insert_game()
        headers = {}

        while True:
            line = pgn_file.readline()

            # we've read to the end of the file
            if not line:
                break
             
            if line.startswith('['):
                # extract field name
                end_field = line.find(' ')
                field = line[1:end_field]

                # find value of field
                start_quote = line.find('"') + 1
                end_quote = line.rfind('"')
                desired_string = line[start_quote:end_quote]

                headers[field] = desired_string
            
            # extracts moves and resets headers
            elif line.startswith('1'):
                headers['Moves'] = line
                # add game to db
                insert_game(cursor, headers)
                conn.commit()
                # reset headers to empty dictionary
                headers = {}
            else:
                continue
#-----------------------------------------------------------------------

'''
Main Function
'''
def main():
    pgn_folder = '/Users/sasha/Desktop/Fall 2024/COS Junior IW/Tang Game Analysis Folder/Games'
    db_path = 'tang_games.db'
    conn = create_db(db_path)

    if conn is not None:
        parse_pgn(pgn_folder, conn)
        conn.close()
    else:
         print("Never created db connection.")

if __name__ == "__main__":
     main()