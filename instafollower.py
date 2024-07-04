from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
import os
import time
from random import randint


def wait(minim=300, maxim=600):
    time.sleep(randint(minim, maxim) / 100)


class InstaFollower:
    def __init__(self):
        self.username = os.environ.get("IG_USERNAME")
        self.password = os.environ.get("IG_PASSWORD")
        self.login_url = "https://www.instagram.com/accounts/login/"
        self.follow_page = "https://www.instagram.com/example.mx"
        self.scroll = 0
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):

        self.driver.get(self.login_url)
        wait()
        for char in self.username:
            wait(minim=5, maxim=10)
            self.driver.find_element(By.XPATH, value="//*[@id='loginForm']/div/div[1]/div/label/input").send_keys(char)

        wait()
        for char in self.password:
            wait(minim=5, maxim=10)
            self.driver.find_element(By.XPATH, value="//*[@id='loginForm']/div/div[2]/div/label/input").send_keys(char)

        wait()
        enter_button = self.driver.find_element(By.XPATH, value="//*[@id='loginForm']/div/div[3]/button")
        enter_button.click()
        wait()

    def find_followers(self):
        self.driver.get(self.follow_page)
        wait()
        followers = self.driver.find_element(By.XPATH, value="//*[contains(text(), 'followers')]")
        followers.click()
        wait()
        self.scroll = int(followers.text.split(" ")[0].replace(",", ""))
        modal_xpath = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]"
        popup_window = self.driver.find_element(By.XPATH, value=modal_xpath)
        scroll_script = 'arguments[0].scrollTop = arguments[0].scrollHeight;'
        for i in range(int(self.scroll/4)):         # For testing purposes
            self.driver.execute_script(scroll_script, popup_window)
        wait()

    def follow(self):
        wait()
        dialog_xpath = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]"
        dialog = self.driver.find_element(By.XPATH, value=dialog_xpath)
        followers = dialog.find_elements(By.TAG_NAME, value="button")
        for follower in followers:
            try:
                follower.click()
                wait()

            except ElementClickInterceptedException:
                cancel = self.driver.find_element(By.XPATH, value="//button[contains(text(), 'Cancel')]")
                cancel.click()
                wait()
