import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from apscheduler.schedulers.background import BackgroundScheduler
import re

excluded_countries = [
    "Australia", "Belgium", "Canada", "Denmark", "England",
    "Finland", "France", "Germany", "Iceland", "Israel",
    "Italy", "Latvia", "Norway", "Portugal", "Qatar",
    "Scotland", "Taiwan", "UAE", "USA"
]
def calculate_percentage_drop(before, after):
    return ((before - after) / before) * 100
def send_telegram_message(bot_token, chat_id, message):
    telegram_api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message,
    }
    response = requests.get(telegram_api_url, params=params)
    return response.json()

def scrape_odds_with_notification(url, div_xpath, additional_drop_elements_xpaths, bot_token, chat_id):
    chrome_driver_path = 'C:\\Users\\Sana\\Desktop\\RussiaOdds\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe'
    chrome_service = ChromeService(chrome_driver_path)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    
    try:
        driver.get(url)
        time.sleep(5)
        
        divs = driver.find_elements(By.XPATH, div_xpath)
        
        # Skip the first element
        divs = divs[1:]

        for div in divs:
            odds_text = div.text
            lines = odds_text.split('\n')
            
            # Extract the required information
            sport = lines[0]
            country = lines[2].strip()  # Line 3: Country
            if country in excluded_countries:
                continue
            league = lines[4]
            teams = f"{lines[8]} - {lines[9]}"
            games_info = lines[5]
            game_date_time = f"{lines[6]}, {lines[7]}"
            odds_section = '\n'.join(lines[12:])
            relevant_value = lines[11] if lines[11] != "B's" else lines[10]
            #percentage = '\n'.join(lines[16:18])
            
            percentage_drop = ""
            percentage_pattern = re.compile(r'\d+\%')  # Regular expression pattern to match percentage values

            #dropped_coefficient = extract_dropped_coefficient(odds_section)  # Extract dropped coefficient
            for line in odds_section:
                match = percentage_pattern.search(line)
                if match:
                    percentage_drop = match.group()
                    break

            if not percentage_drop:
                for line in lines:
                    match = percentage_pattern.search(line)
                    if match:
                        percentage_drop = match.group()
                        break
                      
            # Create a link to OddsPortal using the URL
            #oddsportal_link = f"{div.find_element(By.TAG_NAME, 'a').get_attribute('href')}"
            oddsportal_link_element = div.find_element(By.XPATH, './/a[@class="justify-content flex min-w-0 cursor-pointer items-start justify-start gap-1 next-m:!items-center next-m:!justify-end next-m:!gap-2 w-full"]')
            oddsportal_link = oddsportal_link_element.get_attribute('href')

            # Format and output the information
            
            additional_drop_values = None
            for xpath in additional_drop_elements_xpaths:
                additional_drop_elements = div.find_elements(By.XPATH, xpath)
                if additional_drop_elements:
                    additional_drop_values = [elem.text for elem in additional_drop_elements]
                    break
            
            if additional_drop_values is None:
                additional_drop = "Additional drop values not found."
                difference_text = ""
            else:
                additional_drop = '\n'.join(additional_drop_values)
                
                if len(additional_drop_values) >= 2:
                    last_value = float(additional_drop_values[-1])
                    second_last_value = float(additional_drop_values[-2])
                    difference = last_value - second_last_value
                    difference_text = f"Drop: {difference:.2f}"
                elif len(additional_drop_values) == 1:
                    difference_text = f"Drop: {additional_drop_values[0]}"
                else:
                    difference_text = "Not enough values to calculate difference."
            
            # Combine and format the messages
            game_info = f"\n{game_date_time}\n{sport} - {country} - {league}\n{teams}\n{oddsportal_link}"
            odds_info = f"\n{games_info}Drop {percentage_drop} {relevant_value} "
            telegram_message = f"{game_info}\n{odds_info}"
            
            first_coefficient = float(additional_drop_values[0])
            if first_coefficient <= 10:
            # Sending a notification to Telegram
                    send_telegram_message(bot_token, chat_id, telegram_message)
            
                    # Print to console
                    #print(header)
                    print(odds_section)
                    print(f"Drop information Value:\n{additional_drop}")
                    print(difference_text)
                    print()
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        driver.quit()

# Your Telegram bot token and chat ID
telegram_bot_token = "6485567936:AAHF5Kb5Eyigfok0dnKXXdb5hW_q38BYBVM"
telegram_chat_id = "666052516"

# URLs and XPaths for dropping odds and blocked odds
dropping_odds_url = 'https://www.oddsportal.com/dropping-odds/#overall'
dropping_odds_div_xpath = '//*[@id="app"]/div/div[1]/div/main/div[2]/div[5]/div'
additional_drop_elements_xpaths = [
    ".//div[2]/div/ul/li[2]/div[1]//p",
    "//*[@id='app']/div/div[1]/div/main/div[2]/div[5]/div[31]/div[2]/div/ul/li[2]/div[1]",
    "//*[@id='app']/div/div[1]/div/main/div[2]/div[5]/div[32]/div[2]/div/ul/li[2]/div[3]",
    "//*[@id='app']/div/div[1]/div/main/div[2]/div[5]/div[35]/div[2]/div/ul/li[2]/div[1]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[4]/div[2]/div/ul/li[2]/div[3]",
    "//*[@id='app']/div/div[1]/div/main/div[2]/div[5]/div[2]/div[2]/div/ul/li[2]/div[1]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[8]/div[2]/div/ul/li[2]/div[1]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[9]/div[2]/div/ul/li[2]/div[1]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[10]/div[2]/div/ul/li[2]/div[1]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[11]/div[2]/div/ul/li[2]/div[3]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[14]/div[2]/div/ul/li[2]/div[1]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[15]/div[2]/div/ul/li[2]/div[1]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[17]/div[2]/div/ul/li[2]/div[2]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[18]/div[2]/div/ul/li[2]/div[1]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[19]/div[2]/div/ul/li[2]/div[1]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[21]/div[2]/div/ul/li[2]/div[1]",
    "//*[@id='app']/div/div[1]/div/main/div[2]/div[5]/div[22]/div[2]/div/ul/li[2]/div[1]",
    "//*[@id='app']/div/div[1]/div/main/div[2]/div[5]/div[200]/div[2]/div/ul/li[2]/div[1]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[199]/div[2]/div/ul/li[2]/div[1]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[198]/div[2]/div/ul/li[2]/div[1]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[197]/div[2]/div/ul/li[2]/div[1]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[195]/div[2]/div/ul/li[2]/div[1]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[194]/div[2]/div/ul/li[2]/div[2]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[193]/div[2]/div/ul/li[2]/div[1]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[192]/div[2]/div/ul/li[2]/div[1]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[191]/div[2]/div/ul/li[2]/div[1]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[190]/div[2]/div/ul/li[2]/div[1]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[189]/div[2]/div/ul/li[2]/div[3]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[188]/div[2]/div/ul/li[2]/div[1]"
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[187]/div[2]/div/ul/li[2]/div[2]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[186]/div[2]/div/ul/li[2]/div[1]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[184]/div[2]/div/ul/li[2]/div[1]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[183]/div[2]/div/ul/li[2]/div[1]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[182]/div[2]/div/ul/li[2]/div[2]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[181]/div[2]/div/ul/li[2]/div[1]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[180]/div[2]/div/ul/li[2]/div[2]",
    "/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]/div[179]/div[2]/div/ul/li[2]/div[1]",
    
]

# Create a scheduler
scheduler = BackgroundScheduler()
# Schedule the scrape_and_send function to run every 5 minutes
scheduler.add_job(
    scrape_odds_with_notification,
    'interval',
    minutes=5,
    max_instances=2,  # Limit to 1 instance
    args=[
        dropping_odds_url,
        dropping_odds_div_xpath,
        additional_drop_elements_xpaths,
        telegram_bot_token,
        telegram_chat_id
    ]
)
# Start the scheduler
scheduler.start()

# Keep the script running
# try:
while True:
    time.sleep(1)
# except (KeyboardInterrupt, SystemExit):
