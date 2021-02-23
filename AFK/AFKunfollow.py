# @proh_gram_er

import time
from datetime import datetime
from tkinter import *
from tkinter.ttk import Combobox

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

MAIN = Tk()
MAIN.geometry('1000x400')
MAIN.resizable(False, False)
MAIN.title('AFKunfollow')
MAIN.configure(bg='#424242')

IG_id = StringVar()
IG_password = StringVar()
IG_unfollow = StringVar()
selected_browser = StringVar()


class InstaPy:
    def __init__(self, identity, password, unfollows, browser):
        self.ID = identity
        self.PASSWORD = password
        self.UNFOLLOWS = int(unfollows)
        self.successfully_unfollowed = 0
        if browser == 'Chrome':
            self.BROWSER = webdriver.Chrome(
                executable_path='chromedriver.exe')  # chromedriver
        else:
            self.BROWSER = webdriver.Firefox(
                executable_path='geckodriver.exe')  # firefox driver

    ''' load instagram login page and enter self.ID, self.PASSWORD '''

    def login(self):
        now = datetime.now()
        date_time.config(text=now.strftime('%d/%m/%Y %H:%M:%S'))
        MAIN.update()
        try:
            self.BROWSER.get('https://www.instagram.com')

            # wait till input load
            WebDriverWait(self.BROWSER, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))
            WebDriverWait(self.BROWSER, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))

            # enter self.id and self.PASSWORD into both inputs
            self.BROWSER.find_element_by_xpath(
                "//input[@name='username']").send_keys(self.ID)
            time.sleep(1)
            self.BROWSER.find_element_by_xpath(
                "//input[@name='password']").send_keys(self.PASSWORD)

            # click on login and wait till profile loads
            self.BROWSER.find_element_by_xpath(
                "//button[@type='submit']").click()
            WebDriverWait(self.BROWSER, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[5]/span")))
            print('InstaPy> login successful')
            time.sleep(1)
            self.profile()
        except Exception as error:
            print('InstaPy>', error)
            print('InstaPy> login failed! please check your id and password')
            print('InstaPy> make sure internet is connected')
            self.BROWSER.quit()

    ''' load self.ID profile '''

    def profile(self):
        try:
            self.BROWSER.find_element_by_xpath(
                "//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[5]/span").click()
            WebDriverWait(self.BROWSER, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, f"a[href='/{self.ID}/']")))
            time.sleep(1)
            self.BROWSER.find_element_by_css_selector(
                f"a[href='/{self.ID}/']").click()
            self.unfollow()
        except Exception as error:
            print('InstaPy>', error)
            print('InstaPy> time out to open profile')
            print('InstaPy> make sure internet is connected')
            self.BROWSER.quit()


''' unfollow id followers '''

  def unfollow(self):
       try:

           # wait till following loads then click on following
            WebDriverWait(self.BROWSER, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, f"a[href='/{self.ID}/following/']")))
            time.sleep(1)
            self.BROWSER.find_element_by_css_selector(
                f"a[href='/{self.ID}/following/']").click()
            WebDriverWait(self.BROWSER, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[5]/div/div/div[2]/ul/div')))
            time.sleep(1)

            # click on unfollow button
            while self.successfully_unfollowed != self.UNFOLLOWS:

                # unfollow 10 id and refresh the page
                for idx in range(1, 11):
                    self.BROWSER.find_element_by_xpath(
                        f'/html/body/div[5]/div/div/div[2]/ul/div/li[{idx}]/div/div[3]/button').click()
                    time.sleep(1)
                    self.BROWSER.find_element_by_xpath(
                        "//button[text()='Unfollow']").click()
                    time.sleep(3)
                    print('InstaPy> unfollow successful')
                    self.successfully_unfollowed += 1
                    if self.successfully_unfollowed == self.UNFOLLOWS:
                        break
                    else:
                        time.sleep(2)
                self.BROWSER.refresh()
                time.sleep(5)
                self.unfollow()
            print('InstaPy> successfully unfollowed', self.UNFOLLOWS)
            self.BROWSER.quit()
        except Exception as error:
            print('InstaPy>', error)
            print('InstaPy> something went wrong...')
            print('InstaPy> make sure internet is connected')
            self.BROWSER.quit()


''' check for empty input '''


def valid():
    if len(IG_id.get()) == 0 or len(IG_password.get()) == 0 or len((selected_browser.get())) == 0:
        date_time.config(text='please fill up all details')
        MAIN.update()
    elif str(IG_unfollow.get()).isdigit():
        ref = InstaPy(IG_id.get(), IG_password.get(),
                      IG_unfollow.get(), selected_browser.get())
        ref.login()
    else:
        date_time.config(text='followers should be in digits')
        MAIN.update()


ask_id = Label(MAIN, text='Enter ID', bg='#424242',
               fg='white', width=15, font=('', 15))
id_entry = Entry(MAIN, textvariable=IG_id, bd=3, font=('', 15), width=100)
ask_password = Label(MAIN, text='Enter password',
                     bg='#424242', fg='white', width=15, font=('', 15))
password_entry = Entry(MAIN, textvariable=IG_password,
                       bd=3, font=('', 15), width=100)
ask_unfollows = Label(MAIN, text='Max unfollow',
                      bg='#424242', fg='white', width=15, font=('', 15))
unfollows_entry = Entry(MAIN, textvariable=IG_unfollow,
                        bd=3, font=('', 15), width=25)
ask_browser = Label(MAIN, text='Select  browser',
                    bg='#424242', fg='white', width=15, font=('', 15))
browsers = Combobox(MAIN, font=('', 15), width=25,
                    textvariable=selected_browser, values=['Chrome', 'Firefox'])
start = Button(MAIN, command=valid, text='Start', activebackground='#012014', activeforeground='#00ff00',
               bg='#90ee90', fg='white', height=2, width=10, font=('', 15))
date_time = Label(MAIN, text='', bg='#424242',
                  fg='white', width=25, font=('', 15))
info = Label(MAIN, text='InstaPy is the biggest and most popular Instagram automation tool available for free.\n'
                        'Its incredible range of features makes it the number one tooling to grow your account and\n'
                        'target your core audience in the best possible manner', bg='#424242', fg='white', width=75,
             font=('', 15))
ask_id.grid(row=0, column=0)
id_entry.grid(row=0, column=1)
ask_password.grid(row=1, column=0)
password_entry.grid(row=1, column=1)
ask_unfollows.place(x=0, y=62)
unfollows_entry.place(x=170, y=62)
ask_browser.place(x=500, y=62)
browsers.place(x=675, y=62)
date_time.place(x=350, y=175)
start.place(x=425, y=225)
info.place(x=65, y=300)

MAIN.mainloop()
