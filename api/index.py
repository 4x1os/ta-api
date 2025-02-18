# TA API - Development V1
# Scrape data from TeachAssist Login Credentials

# Imports
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from flask import Flask, request, jsonify
from selenium.webdriver.chrome.options import Options


# Debugging
options = Options()
options.headless = True
app = Flask(__name__) 

# Selenium Scraper
class Browser:
    browser, service = None, None

    # Initialize service and browser
    def __init__(self):
        chromedriver_autoinstaller.install()
        self.service = Service(chromedriver_autoinstaller.get_chrome_driver_path())
        self.browser = webdriver.Chrome(service=self.service)

    # Open url
    def open_page(self, url: str):
        self.browser.get(url)

    # Close url
    def close_browser(self):
        self.browser.close()
    
    # Scan all courses within dashboard
    def scan_courses(self):
        d = self.browser.find_elements(by=By.CLASS_NAME, value='green_border_message')
        print(len(d))
        tbody = d[1].find_element(by = By.TAG_NAME, value='tbody')
        rows = tbody.find_elements(by = By.TAG_NAME, value='tr')
        courses = []
        percentages = []
        for row in rows:
            if (row != rows[0]):
                cells = row.find_elements(By.TAG_NAME, value='td')
                print(len(cells))
                course = cells[0].text.strip()
                courses.append(course)
                mark = cells[2].text.strip()
                for span in cells[2].find_elements(By.TAG_NAME, value='span'):
                    mark = mark.replace(span.text.strip(),"").strip()
                percentages.append(mark)
        return courses, percentages

    #Add credentials
    def add_input(self, by: By, value: str, text: str): 
        # use: find the field using [by] & [value]-> then type in [text]
        field = self.browser.find_element(by=by, value=value)
        field.send_keys(text)
        # time.sleep(1)

    #Submit item
    def click_button(self, by:By, value:str):
        button = self.browser.find_element(by=by, value=value)
        button.click()
        # time.sleep(1)

    #Set a login 
    def login_ta(self, username: str, password: str):
        self.add_input(by=By.NAME, value="username", text=username)
        self.add_input(by=By.NAME, value="password", text=password)
        self.click_button(by=By.NAME, value="submit")
        time.sleep(0.1)
        url = self.browser.current_url
        if "students" in url:
            return True
        else:
            return False

    
@app.route('/')
def home():
    return '<h1> hi guys </h1>'

# Provide User & Password to provide Login Credentials
@app.route('/login', methods = ['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    browser = Browser()
    browser.open_page('https://ta.yrdsb.ca/yrdsb/')
    if browser.login_ta(username, password) == True:
        courses, marks = browser.scan_courses()
        user_data = {
            "courses" : courses,
            "marks" : marks
        }
        browser.close_browser()
        return jsonify(user_data), 200
    else:
        browser.close_browser()
        response = {
            "error" : "invalid credentials"
        }
        return jsonify(response), 400

    
# Run 
if __name__ == '__index__':
    app.run(debug=False)