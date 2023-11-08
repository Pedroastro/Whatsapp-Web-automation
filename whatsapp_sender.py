from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from subprocess import CREATE_NO_WINDOW
import pyautogui
import time
import csv

class whatsappBot:
    def __init__(self):
        self.ser = Service(executable_path="./chromedriver")
        self.ser.creation_flags = CREATE_NO_WINDOW
        self.whatsapp_url = 'https://web.whatsapp.com/'
        self.message_delay = 2

    def send_messages(self, filepath, messages, videos_n_image, documents, actions):

        # Open the CSV file containing the list of people to send messages to
        with open(filepath, mode='r', encoding='utf-8') as contacts_file:
            # Create a CSV reader object
            contacts_reader = csv.reader(contacts_file)

            # Skip the header row
            next(contacts_reader)

            # Open a new Chrome browser window
            driver = webdriver.Chrome(service=self.ser)

            # Navigate to the WhatsApp Web URL
            driver.get(self.whatsapp_url)

            # Wait for the user to scan the QR code and login
            WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="cell-frame-title"]')))
            time.sleep(10)

            notfound_names = []
            notfound_phones = []

            # Loop over each contact in the CSV file
            for row in contacts_reader:

                # Extract the name and phone number from the current row
                name, phone = row

                # if last message did not load wait
                if EC.presence_of_element_located((By.XPATH, '//span[@data-testid="msg-time"]')):
                    time.sleep(1)

                # Find the chat search box and enter the contact name
                search_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
                )
                time.sleep(1)
                search_box = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
                )
                search_box.clear()
                search_box.click()
                search_box.send_keys(Keys.CONTROL + "a")
                search_box.send_keys(Keys.DELETE)
                search_box.send_keys(name)

                try:
                    # Wait for the chat to load and check if the contact exists
                    contact = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, f'//span[@title="{name}"]'))
                    )
                except:
                    # make new lists of names and phones that weren't found
                    notfound_names.append(name)
                    notfound_phones.append(phone)
                    # Log an error message and continue to the next contact
                    print(f'Error: {name} not found.')
                    continue

                # Click on the contact to open the chat
                contact.click()
                time.sleep(2)

                def send_message(message):
                    # if last message did not load wait
                    if EC.presence_of_element_located((By.XPATH, '//span[@data-testid="msg-time"]')):
                        time.sleep(1)
                    if EC.presence_of_element_located((By.XPATH, '//div[@data-testid="conversation-compose-box-input"')):
                        time.sleep(1)

                    # Find the chat box and enter the message
                    try:
                        chat_box = driver.find_element(By.XPATH, '//div[@data-testid="conversation-compose-box-input"]')
                        chat_box.click()
                        chat_box.send_keys(Keys.CONTROL + "a")
                        chat_box.send_keys(Keys.DELETE)
                    except:
                        # make new lists of names and phones that weren't found
                        notfound_names.append(name)
                        notfound_phones.append(phone)
                        # Log an error message and continue to the next contact
                        print(f'Error: {name} blocked.')
                        return

                    if '(name)' in message or '(full name)':
                        newmessage = message.replace('(name)', name.split(' ')[0]).replace('(full name)', name)
                        chat_box.send_keys(newmessage)
                    else:
                        chat_box.send_keys(message)

                    # Find the send button and click it
                    send_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//span[@data-testid="send"]')))
                    send_button.click()

                    # Wait for the message to send
                    WebDriverWait(driver, self.message_delay)

                def send_video_or_image(filepath):
                    # if last message did not load wait
                    if EC.presence_of_element_located((By.XPATH, '//span[@data-testid="msg-time"]')):
                        time.sleep(1)

                    # Click on the attachment icon
                    attachment_icon = driver.find_element(By.XPATH, '//span[@data-testid="clip"]')
                    attachment_icon.click()

                    # Wait for the file input element to appear and then send the file path to it
                    WebDriverWait(driver, 2)
                    # Click on the "Document" button
                    image_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//span[@data-testid="attach-image"]')))
                    image_button.click()
                    time.sleep(1)
                    pyautogui.press('esc')
                    WebDriverWait(driver, 1)
                    document_button = driver.find_element(By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
                    document_button.send_keys(filepath)
                    WebDriverWait(driver, 1)

                    # Find the send button and click it
                    if EC.presence_of_element_located((By.XPATH, '//span[@data-testid="msg-time"]')):
                        time.sleep(1)
                    send_button = WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, '//span[@data-testid="send"]'))
                    )
                    WebDriverWait(driver, 2)
                    send_button.click()
                    time.sleep(3)

                def send_document(filepath):

                    # if last message did not load wait
                    if EC.presence_of_element_located((By.XPATH, '//span[@data-testid="msg-time"]')):
                        time.sleep(1)

                    # Click on the attachment icon
                    attachment_icon = driver.find_element(By.XPATH, '//span[@data-testid="clip"]')
                    attachment_icon.click()

                    # Wait for the file input element to appear and then send the file path to it
                    WebDriverWait(driver, 2)
                    # Click on the "Document" button
                    image_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//span[@data-testid="attach-document"]')))
                    image_button.click()
                    time.sleep(1)
                    pyautogui.press('esc')
                    WebDriverWait(driver, 1)
                    document_button = driver.find_element(By.XPATH, '//input[@accept="*"]')
                    document_button.send_keys(filepath)
                    WebDriverWait(driver, 1)

                    # Find the send button and click it
                    send_button = WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, '//span[@data-testid="send"]'))
                    )
                    WebDriverWait(driver, 2)
                    send_button.click()
                    time.sleep(3)

                messages_count = 0
                videos_n_image_count = 0
                documents_count = 0
                for action in actions:
                    if action == "message":
                        send_message(messages[messages_count])
                        messages_count += 1
                    elif action == "video":
                        send_video_or_image(videos_n_image[videos_n_image_count])
                        videos_n_image_count += 1
                    elif action == "image":
                        send_video_or_image(videos_n_image[videos_n_image_count])
                        videos_n_image_count += 1
                    elif action == "document":
                        send_document(documents[documents_count])
                        documents_count += 1
                    else:
                        print(f"{action} action not valid")

            with open('notfound.csv', mode='w', encoding='utf-8') as notfound_file:
                # Create a CSV writer object
                notfound_writer = csv.writer(notfound_file)

                # Write the header row to the CSV file
                notfound_writer.writerow(['Name', 'Phone'])

                # Write the data rows to the CSV file
                for i in range(len(notfound_names)):
                    print(i)
                    notfound_writer.writerow([notfound_names[i], notfound_phones[i]])

            # Close the browser window
            driver.quit()