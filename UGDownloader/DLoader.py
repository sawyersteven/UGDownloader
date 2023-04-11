import os
import time
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import GUI


def download_tab(driver, url):

    print(f"⬇️ Downloading {url}")
    try:
        # Attempt download via clicking Download button
        driver.get(url)
        scroll_to_bottom(driver)
        button = driver.find_element(By.CSS_SELECTOR, "form[action='https://tabs.ultimate-guitar.com/tab/download'] button")
        button.click()
    except Exception as e:  # sometimes the button is obscured by other elements
        print(e)
        print("⚠️ Can't use download button, using fallback download method")
        download_tab_fallback(driver, url)


def download_tab_fallback(driver, url):
    ''' This method opens the download link directly in the browser instead
    of using the Download Tab button. This can be used when the button doesn't
    exist (removed tab) or is otherwise unusable. This method works almost all
    of the time, but occasionally will only load the tab's interactive page
    instead of a download link. This may happen because the tab doesn't
    actually exist on UG's server. So this should not be used as the primary
    download strategy, but only as a fallback.
    '''
    if driver.current_url != url:
        driver.get(url)

    uid = url.split('-')[-1]
    js_dl = f"window.open('https://tabs.ultimate-guitar.com/tab/download?id={uid}');"
    driver.execute_script(js_dl)
    time.sleep(0.5)


def create_artist_folder(dl_path):
    if os.path.isdir(dl_path):
        print("Using folder at " + dl_path)
        return
    try:
        os.mkdir(dl_path)
    except OSError as error:
        print(error)
    else:
        print("Folder created at " + dl_path)


def scroll_to_bottom(driver):
    # todo check if times can be cut/shortened
    time.sleep(.1)
    driver.execute_script(
        "window.scrollTo(0,document.body.scrollHeight)")  # scroll to bottom of page to see button
    time.sleep(.1)
    driver.execute_script(
        "window.scrollTo(0,document.body.scrollHeight)")  # would be nice to get rid of browser bounce
    time.sleep(.1)
