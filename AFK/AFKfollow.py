# @proh_gram_er

import time
from datetime import datetime
from tkinter import *
from tkinter.ttk import Combobox

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

MAIN = Tk()
MAIN.geometry('1000x500')
MAIN.resizable(False, False)
MAIN.title('AFKfollow')
MAIN.configure(bg='#424242')

IG_id = StringVar()
IG_password = StringVar()
IG_hashtag = StringVar()
IG_comment = StringVar()
IG_followers = StringVar()
selected_browser = StringVar()


class InstaPy:
    def __init__(self, identity, password, hashtag, comment, followers, browser):
        self.ID = identity
        self.PASSWORD = password
        self.HASHTAG = hashtag
        self.COMMENT = comment
        self.FOLLOWERS = int(followers)
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
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']")))
            print('InstaPy> login successful')
            self.hashtag()
        except Exception as error:
            print('InstaPy>', error)
            print('InstaPy> login failed! please check your id and password')
            print('InstaPy> make sure internet is connected')
            self.BROWSER.quit()

    ''' load self.HASHTAG page '''

    def hashtag(self):
        try:
            self.BROWSER.get(
                'https://www.instagram.com/explore/tags/' + self.HASHTAG + '/')
            time.sleep(5)
            hrefs = self.BROWSER.find_elements_by_tag_name('a')

            # fetch all load it posts links
            posts = [href.get_attribute('href') for href in hrefs]
            for post in posts:

                # load individual post and wait till it's load
                self.BROWSER.get(post)
                WebDriverWait(self.BROWSER, 10).until(EC.presence_of_element_located(
                    (By.XPATH,
                     "//*[@id='react-root']/section/main/div/div[1]/article/header/div[2]/div[1]/div[2]/button")))
                time.sleep(1)

                # check if already following or not
                if self.BROWSER.find_element_by_xpath(
                        "//*[@id='react-root']/section/main/div/div[1]/article/header/div[2]/div[1]/div[2]/button") \
                        .text == 'Following':
                    continue

                # else open post profile
                self.BROWSER.find_element_by_tag_name('a').click()
                if self.validation():
                    self.operations()
                else:
                    continue
            print("InstaPy> reached today's all available posts")
            self.BROWSER.quit()
        except Exception as error:
            print('InstaPy>', error)
            print('InstaPy> time out to find hashtag')
            print('InstaPy> make sure internet is connected')
            self.BROWSER.quit()

    ''' checking followers condition '''

    def validation(self):
        try:
            WebDriverWait(self.BROWSER, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "ul")))
            time.sleep(1)
            self.BROWSER.find_element_by_tag_name('ul')
            popularity = self.BROWSER.find_elements_by_tag_name('span')

            # fetching current profile followers
            followers = [amt.get_attribute('title') for amt in popularity]
            if int(re.sub("[',]", '', str(list(filter(None, followers)))[1:-1])) <= self.FOLLOWERS:
                return True
            else:
                return False
        except ElementNotInteractableException:
            self.BROWSER.find_element_by_xpath(
                "//button[text()='Not Now']").click()
        except Exception as error:
            print('InstaPy>', error)
            print('InstaPy> taking too much time')
            print('InstaPy> make sure internet is connected')
            self.BROWSER.quit()

    ''' performing all operations follow, like, comment '''

    def operations(self):
        try:
            self.BROWSER.back()
            time.sleep(2)
            self.BROWSER.find_element_by_xpath(
                "//*[@id='react-root']/section/main/div/div[1]/article/header/div[2]/div[1]/div[2]/button").click()
            print('InstaPy> follow successful')
            time.sleep(2)
            self.BROWSER.find_element_by_xpath(
                "//*[@id='react-root']/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button").click()
            print('InstaPy> like successful')
            time.sleep(2)
            self.BROWSER.find_element_by_tag_name('form').click()
            self.BROWSER.find_element_by_xpath(
                "//textarea[@placeholder='Add a comment…']").send_keys(self.COMMENT)
            time.sleep(2)
            self.BROWSER.find_element_by_xpath(
                "//button[@type='submit']").click()
            print('InstaPy> comment successful')
            print('InstaPy> sleeping for 60 seconds')
            time.sleep(60)
            print('InstaPy> woke up!')
        except NoSuchElementException:
            print('InstaPy> comments are disabled')
            print('InstaPy> sleeping for 60 seconds')
            time.sleep(60)
            print('InstaPy> woke up!')
        except ElementNotInteractableException:
            self.BROWSER.find_element_by_xpath(
                "//button[text()='Not Now']").click()
        except Exception as error:
            print('InstaPy>', error)
            print('InstaPy> taking too much time')
            print('InstaPy> make sure internet is connected')


''' check for empty input '''


def valid():
    if len(IG_id.get()) == 0 or len(IG_password.get()) == 0 or len(IG_hashtag.get()) == 0 or len(
            IG_comment.get()) == 0 or len((selected_browser.get())) == 0:
        date_time.config(text='please fill up all details')
        MAIN.update()
    elif str(IG_followers.get()).isdigit():
        ref = InstaPy(IG_id.get(), IG_password.get(), IG_hashtag.get(), IG_comment.get(), IG_followers.get(),
                      selected_browser.get())
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
ask_tags = Label(MAIN, text='Enter hashtag', bg='#424242',
                 fg='white', width=15, font=('', 15))
tag_entry = Entry(MAIN, textvariable=IG_hashtag,
                  bd=3, font=('', 15), width=100)
ask_comments = Label(MAIN, text='Enter comment', bg='#424242',
                     fg='white', width=15, font=('', 15))
comment_entry = Entry(MAIN, textvariable=IG_comment,
                      bd=3, font=('', 15), width=100)
ask_followers = Label(MAIN, text='Max followers',
                      bg='#424242', fg='white', width=15, font=('', 15))
followers_entry = Entry(MAIN, textvariable=IG_followers,
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
ask_tags.grid(row=2, column=0)
tag_entry.grid(row=2, column=1)
ask_comments.grid(row=3, column=0)
comment_entry.grid(row=3, column=1)
ask_followers.place(x=0, y=125)
followers_entry.place(x=170, y=125)
ask_browser.place(x=500, y=125)
browsers.place(x=675, y=125)
date_time.place(x=350, y=225)
start.place(x=425, y=275)
info.place(x=65, y=400)

MAIN.mainloop()
