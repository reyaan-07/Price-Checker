from datetime import datetime 
from web_url import ProductPrice
from dcsc_url import ConfigurationPrice
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor

def get_web_price(web_url):
    try:
        web_obj = ProductPrice(web_url)
        return web_url, web_obj.get_product_price()
    except Exception as e:
        print(f"Failed to extract price from {web_url} : {e}")
        return web_url, None

def get_dcsc_price(dcsc_url):
    try:
        dcsc_obj = ConfigurationPrice(dcsc_url)
        return dcsc_url, dcsc_obj.get_configuration_price()
    except Exception as e:
        print(f"Failed to extract price from {dcsc_url} : {e}")
        return dcsc_url, None

def process_file(file_path):
    print(f"Processing file: {file_path}")
    sheets = pd.read_excel(file_path, sheet_name=None)
    processed_sheets = {}
    overall_sheets = {}
    start = time.time()
    
    try:
        for sheet_name, df in sheets.items():
            print(f"Processing sheet: {sheet_name}")
            web_urls = df['Web URL']
            dcsc_urls = df['DCSC URL']
            web_prices = []
            dcsc_prices = []

            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = []
                for web_url, dcsc_url in zip(web_urls, dcsc_urls):
                    futures.append(executor.submit(get_web_price, web_url))
                    futures.append(executor.submit(get_dcsc_price, dcsc_url))

                for i in range(0, len(futures), 2):
                    web_future = futures[i]
                    dcsc_future = futures[i + 1]
                    web_url, web_price = web_future.result()
                    dcsc_url, dcsc_price = dcsc_future.result()
                    web_prices.append(web_price)
                    dcsc_prices.append(dcsc_price)

            processed_df = pd.DataFrame({'Web URL': web_urls, 'DCSC URL': dcsc_urls, 'Web Price': web_prices, 'DCSC Price': dcsc_prices})
            overall_sheets[sheet_name] = processed_df
            processed_df = processed_df[processed_df['Web Price'] != processed_df['DCSC Price']]
            processed_sheets[sheet_name] = processed_df

        today = datetime.now().strftime('%Y-%m-%d')
        output_file_mismatch = f'./output/Extracted_Price_Mismatch_{today}.xlsx'
        output_file_overall = f'./output/Overall_Extracted_Data_{today}.xlsx'

        with pd.ExcelWriter(output_file_mismatch) as writer:
            for sheet_name, processed_df in processed_sheets.items():
                processed_df.to_excel(writer, sheet_name=sheet_name, index=False)

        with pd.ExcelWriter(output_file_overall) as writer:
            for sheet_name, overall_df in overall_sheets.items():
                overall_df.to_excel(writer, sheet_name=sheet_name, index=False)

        finish = (time.time() - start) / 60
        print(f"Task finished in {finish} mins.")
        return output_file_mismatch  # Return the path of the output file
    except Exception as e:
        print(f"Code execution failed: {e}")
        return None