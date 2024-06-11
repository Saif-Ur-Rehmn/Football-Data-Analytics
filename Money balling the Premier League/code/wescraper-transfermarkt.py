import requests
from bs4 import BeautifulSoup
import csv

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

def scrape_transfermarkt(page_num):
    url = f"https://www.transfermarkt.com/premier-league/marktwertaenderungen/wettbewerb/GB1/page/{page_num}"
    try:
        # Send a GET request to the URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for request errors

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Print the title of the page to verify we're on the correct page
        print(f"Page title: {soup.title.string}")

        # Find the table containing player data
        table = soup.find('table', {'class': 'items'})

        if not table:
            print(f"No data found on page {page_num}")
            return []

        # Initialize lists to store player names, market values, and clubs
        players = []
        market_values = []
        clubs = []

        # Extract player names, market values, and clubs from the table rows
        for row in table.find_all('tr', {'class': ['odd', 'even']}):
            player_name_tag = row.find('td', {'class': 'hauptlink'})
            market_value_tag = row.find('td', {'class': 'rechts hauptlink'})
            club_tag = row.find('td', {'class': 'zentriert'}).find('a')

            if player_name_tag and market_value_tag and club_tag and 'title' in club_tag.attrs:
                player_name = player_name_tag.get_text(strip=True)
                market_value = market_value_tag.get_text(strip=True)
                club = club_tag['title']

                players.append(player_name)
                market_values.append(market_value)
                clubs.append(club)

        # Combine player names, market values, and clubs into a list of tuples
        player_data = list(zip(players, market_values, clubs))

        return player_data

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred on page {page_num}: {http_err}")
    except Exception as err:
        print(f"An error occurred on page {page_num}: {err}")

    return []

def save_to_csv(data, filename):
    # Define the header
    header = ['Player', 'Market Value', 'Club']
    
    try:
        # Open the file in write mode with utf-8 encoding
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Write the header
            writer.writerow(header)
            
            # Write the data
            writer.writerows(data)
        
        print(f"Data successfully saved to {filename}")
    
    except Exception as e:
        print(f"An error occurred while saving to CSV: {e}")

# Main script to scrape pages 1 to 22 and save the data to a CSV file
all_player_data = []

for page_number in range(1, 23):
    print(f"Scraping page {page_number}...")
    player_data = scrape_transfermarkt(page_number)
    all_player_data.extend(player_data)

# Save the combined data to a CSV file
save_to_csv(all_player_data, 'player_market_values_all_pages_and_eplclubs.csv')
