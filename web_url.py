import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

class ProductPrice:
    def __init__(self, product_url):
        self.product_url = product_url
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

    def get_product_price(self):
        while self.try_number < 3:
            driver = None
            try:
                driver = self.initiate_driver()
                return self.initiate_product_price_extraction(driver)
            except Exception as e:
                self.try_number += 1
                wait_time = 2 ** self.try_number  # Exponential backoff
                print(f"Exception occurred in product_price.py initiate_extraction : {e} Try #{self.try_number}/3. Retrying in {wait_time} seconds.")
                time.sleep(wait_time)
            finally:
                if driver:
                    driver.quit()
        print(f"The element might not be there. Have a look at the Web URL: {self.product_url}")
        return None

    def initiate_product_price_extraction(self, driver):
        # Open the webpage
        driver.get(self.product_url)
        driver.maximize_window()
        time.sleep(15)

        try:
            # Getting the price element
            product_price = driver.find_element(By.XPATH,'//*[@id="9e2b7750d16d4-4f63-872e-1857d46ca8b1"]/div[1]/div[2]/div/div[2]/div[2]/div[3]/div[1]/span[2]')
        except Exception as e:
            try:
                # If the general price is there not the est value i.e lined out
                product_price = driver.find_element(By.XPATH,'//*[@id="9e2b7750d16d4-4f63-872e-1857d46ca8b1"]/div[1]/div[2]/div/div[2]/div[2]/div[3]/div[3]/div[1]/div[1]/span[1]')
            except Exception as e:
                try:
                    # ISG price
                    product_price = driver.find_element(By.XPATH,'//*[@id="5c4105e9p425f-4e51-a54d-0740b919ce70"]/div[3]/div[2]/div/div/div[1]/div[1]/div[4]/div[2]/div[1]/div/span[3]')
                except Exception as e:
                    try:
                        # If the price element is on the left side
                        product_price = driver.find_element(By.XPATH,'//*[@id="a6fdc8c7uea7e-42ac-b05a-79c0a62a7745"]/div[3]/div[2]/div/div/div[1]/div[1]/div[4]/div[2]/div[1]/div/span[3]')
                    except Exception as e:
                        # Servers watch tour interface
                        driver.execute_script('window.scrollBy(0,1000);')
                        product_price = driver.find_element(By.XPATH,'//*[@id="6ec684e19649a-471f-af12-1b4675647a9b"]/div[2]/div[2]/div[4]/div[2]/section/div/ul/li/div[2]/div/div[2]/div[1]/div/div[1]/div/span[3]')
        
        # Get the price text
        product_price = product_price.text
        product_price = product_price.split('$')[1]
        product_price = [digit for digit in product_price if digit != ',']
        product_price = float(''.join(product_price))
        return product_price


# if __name__ == "__main__":
#     obj = ProductPrice("https://www.lenovo.com/ca/en/p/servers-storage/storage/das/thinksystem-d4390-direct-attached-storage/7dah1000na")
#     print(obj.get_product_price())