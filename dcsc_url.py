import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

class ConfigurationPrice:
    def __init__(self, config_url):
        self.config_url = config_url
        self.try_number = 0

    def initiate_driver(self):
        chrome_driver_path = "chromedriver.exe"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = True
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(120)  # Set page load timeout to 120 seconds
        return driver

    def get_configuration_price(self):
        while self.try_number < 3:
            driver = None
            try:
                driver = self.initiate_driver()
                return self.initiate_config_price_extraction(driver)
            except Exception as e:
                self.try_number += 1
                wait_time = 2 ** self.try_number  # Exponential backoff
                print(f"Exception occurred in configuration_price.py initiate_extraction : {e} Try #{self.try_number}/3. Retrying in {wait_time} seconds.")
                time.sleep(wait_time)
            finally:
                if driver:
                    driver.quit()
        print(f"The element might not be there. Have a look at the DCSC URL: {self.config_url}")
        return None
    
    def initiate_config_price_extraction(self, driver):
        # Open the webpage
        driver.get(self.config_url)
        driver.maximize_window()
        time.sleep(15)

        try:
            # Switching to the iframe containing the required element
            required_iframe = driver.find_element(By.ID, "dcgIframe")
            driver._switch_to.frame(required_iframe)

            try:
                # Getting the price
                config_price = driver.find_element(By.ID, 'webprice')
            except Exception as e:
                # If lined price is not there and only summary price is there
                config_price = driver.find_element(By.XPATH,'//*[@id="entry"]/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div[3]/div/div/span')

        except Exception as e:
            # If the checkbox interface is there
            driver.execute_script('window.scrollBy(0,500);')

            dropdown = driver.find_element(By.XPATH, '//*[@id="summary"]/div[2]/div[2]/div[1]')
            dropdown.click()

            try:
                # If lined out price is there
                config_price = driver.find_element(By.XPATH, '//*[@id="summary"]/div[2]/div[2]/div[2]/div/div[2]/span')
            except Exception as e:
                # If normal non-lined out price is there
                config_price = driver.find_element(By.XPATH, '//*[@id="summary"]/div[2]/div[2]/div[2]/div/div[2]')

        # Get the price text
        config_price = config_price.text
        config_price = config_price.split('$')[1]
        config_price = [digit for digit in config_price if digit != ',']
        config_price = float(''.join(config_price))
        return config_price
    
# if __name__ == "__main__":
#     obj = ConfigurationPrice("https://www.lenovo.com/ca/en/configurator/dcg/index.html?lfo=7DAH1000NA")
#     print(obj.get_configuration_price())