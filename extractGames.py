'''
Extracts all of Tang's games since 2013
Author: Sasha Khoretonenko
'''

import requests
import os
import datetime
import numpy as np

# Set your email for the User-Agent header
email = "sasha.khoretonenko@gmail.com"
headers = {
    'User-Agent': email
}

'''
Get pgn data for a specific player for a specific month and year.
'''
def download_pgn(username, year, month, save_path):
    # Ensure month is two digits
    month = f"{int(month):02d}"
    
    # url for downloading pgn
    url = f"https://api.chess.com/pub/player/{username}/games/{year}/{month}/pgn"

    # Send a request to download the PGN
    response = requests.get(url, headers=headers)

    # Check if request was successful
    if response.status_code == 200:
        # Save the PGN to a file
        filename = f"{username}_{year}_{month}.pgn"
        full_path = os.path.join(save_path, filename)

        # Save pgn to specified path
        with open(full_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded PGN file and saved as {full_path}")

    else:
        print(f"Failed to download PGN. Status code: {response.status_code}")


'''
Main Function
'''
def main():
    # Downloads all games dating back to 2013
    for year in range(2014, 2025):
        save_directory = f'/Users/sasha/Desktop/Fall 2024/COS Junior IW/Tang Game Analysis Folder/Games/{year} Games'
        for month in range(1, 13):
            download_pgn('penguingm1', year, month, save_directory)

if __name__ == "__main__":
    main()