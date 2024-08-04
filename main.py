import constants
import notifications

import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import selenium.common.exceptions

# Create a new instance of the Chrome driver
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_experimental_option("detach", True)
# options.add_argument("--start-maximized")
driver = webdriver.Chrome(options)

DZRT_EMAIL = constants.ACCOUNT_ID1[0]
DZRT_PASS  = constants.ACCOUNT_ID1[1]

######################################################################

# Login Bypass
def LoginHandler():
    if ( 'login' not in driver.current_url):
        driver.get("https://www.dzrt.com/en/customer/account/login/")
    
    while( 'login' in driver.current_url ):
        
        ObstaclesBypass()

        if len(driver.find_elements(By.ID, 'email')) > 0: 
            email = driver.find_element(By.ID, 'email')
        elif len(driver.find_elements(By.ID, 'customer-email')) > 0: 
            email = driver.find_element(By.ID, 'customer-email')
        else: 
            driver.refresh()
        
        password = driver.find_element(By.ID, 'pass')

        email.clear()
        password.clear()

        email.send_keys(DZRT_EMAIL)
        password.send_keys(DZRT_PASS)
        
        try:
            driver.find_element(By.ID, 'send2').submit()
        except:
            pass

# Age Checker Panel Remover
def AgeConformationHandler():
    btn = driver.find_element(By.CLASS_NAME, 'upper-age')
    if btn.is_displayed():
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'upper-age'))).click()
        except selenium.common.exceptions.ElementClickInterceptedException:
            ActionChains(driver).move_by_offset(btn.location["x"], btn.location["y"]).click().perform()

# Cookies panel Remover
def CookiesPanelHandler():
    btn = driver.find_element(By.CLASS_NAME, 'm-decline')
    if btn.is_displayed():
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'm-decline'))).click()
        except selenium.common.exceptions.ElementClickInterceptedException:
            ActionChains(driver).move_by_offset(btn.location["x"], btn.location["y"]).click().perform()

# Navigate to a website
def AddToCart():
    
    if ( 'icy-rush' not in driver.current_url):
        driver.get("https://www.dzrt.com/en/icy-rush.html")

    while( 'icy-rush' in driver.current_url ):
        
        ObstaclesBypass()

        addButton = driver.find_elements(By.ID, 'product-addtocart-button')

        if len(addButton) > 0:
            ActionChains(driver).move_to_element(addButton[0]).perform()
            addButton[0].click()
            notifications.NotifyMe("Is Added")
            Core()
        else:
            driver.refresh()

def Cart():

    if ( 'cart' not in driver.current_url):
        driver.get("https://www.dzrt.com/en/checkout/cart/")

    notifications.NotifyMe("In Cart")

    while( 'cart' in driver.current_url ):
        
        ObstaclesBypass()
        
        checkoutButton = driver.find_elements(By.XPATH, "//button[@data-role='proceed-to-checkout']")
        
        if len(checkoutButton) > 0:
            
            notifications.NotifyMe("It's Available")

            qty = driver.find_element(By.XPATH, "//input[@title='Qty']")

            if(qty.get_attribute('value') != '5'):
                qty.clear()
                qty.send_keys("5")
                qty.send_keys(Keys.ENTER)
                continue
            
            # ActionChains(driver).move_to_element(checkoutButton[0]).click().perform()
            CheckOut()
        else:
            driver.refresh()

def CheckOut():
    
    notifications.NotifyMe("Product is available")
    
    driver.get("https://www.dzrt.com/en/onestepcheckout.html")
    
    while True:
        isLoading = driver.find_elements(By.CLASS_NAME, 'loading-mask')
        
        if(len(isLoading) > 0):
            continue

        if( 'onestepcheckout' in driver.current_url ):
            payment = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='aps_fort_cc']")))
            ActionChains(driver).move_to_element(payment).click().perform()

            card = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.payment-method-title.field.choice.vault')))
            ActionChains(driver).move_to_element(card).click().perform()

            ccv = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".label.label-cvv")))
            ActionChains(driver).move_to_element(ccv).send_keys("745").perform()

            btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-placeorder")))
            ActionChains(driver).move_to_element(btn).click().perform()
            break


# Bypass obstacles in the website such as pop-ups
def ObstaclesBypass():
    
    if len(driver.find_elements(By.CLASS_NAME, 'upper-age')) > 0:
        AgeConformationHandler()

    if len(driver.find_elements(By.CLASS_NAME, 'm-decline')) > 0:
        CookiesPanelHandler()

def Core():
    
    while True:
        ObstaclesBypass()
        
        while True:
            try:
                localStorage = driver.execute_script("return JSON.parse(window.localStorage['mage-cache-storage'])")
                break
            except:
                pass
        
        if len(localStorage) == 0:
            LoginHandler()
            continue
        
        if localStorage['cart']['summary_count'] > 0:
            Cart()
        else:
            AddToCart()

def main():
    
    while True:
        if(time.localtime().tm_hour > 12 or True):
            notifications.NotifyMe("Bot has started")
            break
    driver.get("https://www.dzrt.com/en/")
    Core()

if __name__ == "__main__":
    main()