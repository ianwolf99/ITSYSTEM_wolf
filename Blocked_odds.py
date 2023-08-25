import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from apscheduler.schedulers.background import BackgroundScheduler

def send_message_to_telegram_bot(bot_token, chat_id, message,label):
    labeled_message = f"{label}\n\n{message}"
    telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    # Split the message into chunks of a specified length
    max_chunk_length = 4000
    message_chunks = [message[i:i + max_chunk_length] for i in range(0, len(message), max_chunk_length)]
    
    for chunk in message_chunks:
        data = {
            "chat_id": chat_id,
            "text": chunk
        }
        try:
            response = requests.post(telegram_url, json=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while sending the message: {str(e)}")
            print("Response content:", response.content)
            return False
    return True

def scrape_and_send():
    chrome_driver_path = 'C:\\Users\\Sana\\Desktop\\RussiaOdds\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe'
    chrome_service = ChromeService(chrome_driver_path)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    try:
        url = 'https://www.oddsportal.com/blocked/'
        driver.get(url)
        time.sleep(5)
        
        blocked_odds_xpath = '/html/body/div[1]/div/div[1]/div/main/div[2]/div[5]'
        blocked_odds_element = driver.find_element(By.XPATH, blocked_odds_xpath)
        blocked_odds_text = blocked_odds_element.text
        
        bot_token = "6485567936:AAHF5Kb5Eyigfok0dnKXXdb5hW_q38BYBVM"
        chat_id = "666052516"
        label = "Blocked Odds:"  # Label indicating blocked odds
        send_result = send_message_to_telegram_bot(bot_token, chat_id, blocked_odds_text, label)
        #send_result = send_message_to_telegram_bot(bot_token, chat_id, blocked_odds_text)
        
        if send_result:
            print("Blocked odds sent to Telegram successfully.")
        else:
            print("Failed to send blocked odds to Telegram.")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        driver.quit()

# Create a scheduler
scheduler = BackgroundScheduler()
# Schedule the scrape_and_send function to run every 15 minutes
scheduler.add_job(scrape_and_send, 'interval', minutes=15)
# Start the scheduler
scheduler.start()

# Keep the script running
try:
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    # Shut down the scheduler gracefully when stopping the script
    scheduler.shutdown()