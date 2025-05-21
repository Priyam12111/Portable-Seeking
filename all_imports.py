# Core modules
import os
import random
import re
import sys
import time
import zipfile
import subprocess
from datetime import date
from shutil import move, copymode, make_archive
# Selenium modules
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from webdriver_manager.chrome import ChromeDriverManager

# ChromeDriver setup
def setup_driver():
    opt = Options()
    opt.add_experimental_option("debuggerAddress", "localhost:8989")
    opt.add_argument("--start-maximized")
    opt.add_argument('--disable-blink-features=AutomationControlled')
    
    # Enhanced fingerprint protection
    opt.add_argument("--disable-webgl")  # WebGL fingerprint protection
    opt.add_argument("--disable-site-isolation-trials")
    opt.add_argument("--disable-features=IsolateOrigins,site-per-process")
    opt.add_argument("--disable-3d-apis")
    opt.add_argument("--disable-web-security")
    opt.add_argument("--disable-dev-shm-usage")
    opt.add_argument("--no-sandbox")
    opt.add_argument("--disable-notifications")
    opt.add_argument(f"--user-data-dir={os.path.expanduser('~')}/chrome_profiles/profile_{random.randint(1,100)}")
    # Set realistic user agent
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    opt.add_argument(f'--user-agent={user_agent}')


    # Disable automation flags
    # opt.add_experimental_option("excludeSwitches", ["enable-automation", "load-extension"])
    # opt.add_experimental_option("useAutomationExtension", False)

    # Optional: Use existing browser profile (create one manually first)
    # opt.add_argument("--user-data-dir=/path/to/your/chrome/profile")

    # Optional: For headless mode (uncomment if needed)
    # opt.add_argument('--headless=new')  # New headless mode in Chrome 109+
    # opt.add_argument('--window-size=1920,1080')  # Set resolution when headless
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=opt
    )

    driver.implicitly_wait(2)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        window.navigator.chrome = {
            app: {},
            runtime: {},
        };
        """
    })
    return driver

# Utility functions
def tab(n, driver):
    tn = driver.window_handles[n]
    driver.switch_to.window(tn)

def wait_for_clickable(xpth, driver):
    return WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpth)))

def find_element(xpath, driver):
    try:
        return driver.find_element(by=By.XPATH, value=xpath)
    except Exception:
        return None

def wrreplace(cpth, search_text, replace_text, r_factor=1):
    with open(cpth, 'r+') as f:
        file = f.read()
        
        # Split on search_text
        parts = re.split(f'({search_text})', file)
        
        # Find all the search_text occurrences
        matches = [i for i, x in enumerate(parts) if x == search_text]
        
        if r_factor <= len(matches):
            # Replace the r_factor'th occurrence
            parts[matches[r_factor-1]] = replace_text
            file = ''.join(parts)
            
            f.seek(0)
            f.write(file)
            f.truncate()
        else:
            raise ValueError(f"Only {len(matches)} occurrences found")

def write(cont):
    with open('extract.csv', 'a', encoding='utf-8') as f:
        try:
            f.write(cont)
        except:
            pass

def wait_for_presence(xpth, driver):
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpth)))

def scroll(driver):
    driver.execute_script("window.scrollBy(0, 500);")  # Scroll down by 500 pixels
  