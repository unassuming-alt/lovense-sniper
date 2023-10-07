import threading
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import PySimpleGUI as sg
import json

# Global variables
pause_flag = True
last_user = None

# Load the configuration file
try:
    with open('config.json') as json_file:
        config = json.load(json_file)
except FileNotFoundError:
    config = None

# Set global variables based on whether config was successfully loaded
if config is not None:
    cookie = config['cookie']
    users_file = config['users_file']
else:
    cookie = None
    users_file = None

def ready_browser():
    global driver
    driver = webdriver.Chrome()
    driver.get('https://lovenselife.com/')
    driver.add_cookie({'name' : 'lovenseclub', 'value' : cookie})
    driver.refresh()

def pause(window=None):
    global pause_flag
    pause_flag = True
    if window:
        window['-LED-'].update(background_color='red', text_color='red')

def read_targets(users_file):
    target_users = []
    with open(users_file, 'r') as file:
        for line in file:
            target_users.append(line.strip())
    return target_users


def get_page_source(driver):
    html = driver.page_source
    return BeautifulSoup(html, 'html.parser')

def find_messages(soup):
    outer_div = soup.find('div', {'class': 'chatpanels chat_list_box'})
    inner_div = outer_div.find('div', {'class': 'chat_m chat_c chat-messages'})
    return inner_div.find_all('div', {'class': 'message-item chat_left'})

def check_last_message(message_divs, target_users, driver, window):
    global pause_flag, last_user
    if message_divs:
        message_div = message_divs[-1]
        username = message_div.find('p', {'class': 'chat_name'}).text.strip()
        if username in target_users:
            link = message_div.find('a', href=lambda href: href and "https://c.lovense-api.com/t2/" in href)
            if link:
                # Open link in a new tab
                driver.execute_script(f"window.open('{link['href']}', '_blank')")
                last_user = username
                window['-LAST_USER-'].update(last_user)  # Update 'Last User:' field
                window.refresh()  # Force GUI to update immediately
                pause(window)  # Set pause_flag to True and update LED color

def finder(window):
    global pause_flag, driver

    pause_flag = False
    window['-LED-'].update(background_color='green' if not pause_flag else 'red', text_color='green' if not pause_flag else 'red')
    
    target_users = read_targets(users_file)

    while not pause_flag:
        soup = get_page_source(driver)
        message_divs = find_messages(soup)
        check_last_message(message_divs, target_users, driver, window)

        time.sleep(0.1)

def main():
    global cookie, users_file, last_user
    # Define the window's contents
    layout = [[sg.Text("Enter Lovenselife Cookie"), sg.Input(default_text=cookie if config else '', key='-COOKIE-', password_char='*')],
      [sg.Text('Select the users file'), sg.Input(default_text=users_file if config else '', key='-FILE-', enable_events=True), sg.FileBrowse()],
      [sg.Button('Launch Browser'), sg.Button('Start'), sg.Button('Stop'), sg.Button('Quit')],
      [sg.Text('     ', key='-LED-', background_color='red', text_color='red'), sg.Text('Opened link from user:'), sg.Text(size=(40,1), key='-LAST_USER-')]]


    # Create the window
    window = sg.Window('Lovense Sniper', layout)

    # Event loop
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break
        elif event == 'Launch Browser':
            cookie = values['-COOKIE-']
            ready_browser()
        elif event == 'Start':
            users_file = values['-FILE-']
            finder_thread = threading.Thread(target=finder, args=(window,), daemon=True)
            finder_thread.start()
        elif event == 'Stop':
            pause(window)
        window['-LAST_USER-'].update(last_user)

    # Finish up by removing from the screen
    window.close()

if __name__ == "__main__":
    main()