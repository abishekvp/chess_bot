
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import keyboard, threading, time


driver = webdriver.Firefox()
action = ActionChains(driver)
driver_wait = WebDriverWait(driver, 10)

def open_site(url):driver.get(url)
def new_win():driver.execute_script("window.open('');")
def switch_win(win):driver.switch_to.window(driver.window_handles[win])
def close_win():driver.close()

def child_proccess():pass
# threading.Thread(name='child procs', target=child_proccess).start()
def listen(key):
    while True:
        keyboard.wait(key)
        if key=="esc":start(f_move=False)
threading.Thread(target=listen, kwargs={"key":"esc"}).start()

def class_click(_class):
    try:
        driver.find_element(By.CLASS_NAME,_class).click()
        return True
    except:class_click(_class)


def click_btn(xpath):
    try:
        driver.find_element(By.XPATH,xpath).click()
        return True
    except:click_btn(xpath)


def send_value(xpath,value):
    try:
        driver.find_element(By.XPATH,xpath).send_keys(value)
        return True
    except:send_value(xpath,value)

def login():
    driver.get('https://www.chess.com/login_and_go?returnUrl=https://www.chess.com/play/computer')
    send_value(xpath='//*[@id="username"]',value='asrif420@email.com')
    send_value(xpath='//*[@id="password"]',value='Asrif420#value')
    click_btn('//*[@id="login"]')


def getting_ready(f_move):
    open_site(url="https://www.chess.com/play/computer/Komodo25")
    new_win()
    switch_win(1)
    open_site(url="https://www.chess.com/play/computer/Komodo25")


def listen_board(win, last_highlight):
    switch_win(win)
    dynamic_content = driver_wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="board-play-computer"]')))
    dynamic_content = dynamic_content.get_attribute("outerHTML")
    dynamic_content = BeautifulSoup(dynamic_content, 'html.parser')
    sq0, sq1 = dynamic_content.find_all(class_="highlight")[0], dynamic_content.find_all(class_="highlight")[1]
    sq0, sq1 = str(sq0).split('"')[1].split(" ")[1], str(sq1).split('"')[1].split(" ")[1]
    print("listen board",sq1+sq0, last_highlight)
    if sq0+sq1==last_highlight:
        time.sleep(1)
        listen_board(win)
    else:return True

def scrape_board(win):
    switch_win(win)
    dynamic_content = driver_wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="board-play-computer"]')))
    dynamic_content = dynamic_content.get_attribute("outerHTML")
    dynamic_content = BeautifulSoup(dynamic_content, 'html.parser')
    sq0, sq1 = dynamic_content.find_all(class_="highlight")[0], dynamic_content.find_all(class_="highlight")[1]
    sq0, sq1 = str(sq0).split('"')[1].split(" ")[1], str(sq1).split('"')[1].split(" ")[1]
    print("scrap in ",win, sq0, sq1)
    if win==1:win=0
    elif win==0:win=1
    move_coin(sq0=sq0, sq1=sq1, win=win)

def move_coin(sq0, sq1, win):
    try:
        switch_win(win)
        print("move in",win, sq0, sq1)
        driver.find_element(By.CLASS_NAME,sq0).click()
        # driver_wait.until(EC.presence_of_element_located((By.CLASS_NAME,sq1)))
        action.move_to_element(driver.find_element(By.CLASS_NAME,sq1)).click().perform()
        last_highlight=sq0+sq1
        if listen_board(win,last_highlight):scrape_board(win)
    except:
        time.sleep(5)
        move_coin(sq1, sq0, win)

def func_main(win, last_highlight):
    while True:
        ch=listen_board(win, last_highlight)
        print("main chk",ch)
        if ch:
            print("last highlight pre : ",last_highlight)
            last_highlight=scrape_board(win)
            print("last highlight after : ",last_highlight)
            if win==0:win=1
            elif win==1:win=0
        time.sleep(2)


getting_ready(f_move=True)
input("Enter to start")
board=0
last_highlight = ""
func_main(win=board, last_highlight=last_highlight)
