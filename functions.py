import os
import glob
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from math import floor, ceil
from datetime import timedelta, date
from selenium.webdriver.common.by import By
from xls2xlsx import XLS2XLSX
from dotenv import load_dotenv

# Load environment variables from a .env file if using python-dotenv
load_dotenv()

download_directory = os.path.abspath("C:/Users/Admin/Downloads/cac_chat")
USERNAMES = [
    os.getenv("USERNAME_1"),
    os.getenv("USERNAME_2"),
    os.getenv("USERNAME_3"),
    os.getenv("USERNAME_4"),
]

PASSWORDS = [
    os.getenv("PASSWORD_1"),
    os.getenv("PASSWORD_2"),
    os.getenv("PASSWORD_3"),
    os.getenv("PASSWORD_4"),
]

chat_index = {'acesulfame k': 1, 'aspartame': 2, 'sucralose': 3,
              'malic acid': 4, 'I+G': 5, 'gelatin': 6, 'xanthan': 7,
              'konjac': 8, 'tartrazine': 9, 'sorbate': 10, 'yeast extract': 11,
              'huong thit': 12, 'sodium dehydroacetate': 13, 'bột làm thạch': 14,
              'hfcs': 15,  'gluten': 16, 'soy protein': 17, 'acid ascorbic': 18,
              'inositol': 19, 'vitamin c': 20, "taurine": 21,
              "pectin": 22, "sodium carboxymethyl cellulose": 23, "sorbic acid": 24, "gellan gum": 25,
              "beta cyclodextrin": 26, "calcium lactate": 27, "calcium propionate": 28, 'erythritol': 29, "ponceau": 30,
              "potassium chloride": 31, "sodium polyphosphate": 32, "tripotassium citrate": 33, "ethyl maltol": 34,
              'sodium cyclamate': 35, 'trisodium citrate': 36, 'sodium saccharin': 37, 'locust bean gum': 38,
              'sodium stearoyl lactylate': 39, 'pentasodium triphosphate': 40, 'collagen': 41, 'sodium erythorbate': 42,
              'guar gum': 43, 'sodium alginate': 44, 'trehalose': 45, 'inulin': 46, 'natural color': 47, 'propylene glycol alginate': 48}


def take_index(chat):
    try:
        return chat_index[chat]
    except:
        chat_index[chat] = max(chat_index.values())+1
        return max(chat_index.values())

def move_to_download_folder(downloadPath, newFileName, fileExtension):
    got_file = False
    install_status = True  # file is not downloaded so nothing has been found
    # Grab current file name.
    # interupt=1
    while not got_file:
        try:
            currentFiles = glob.glob(downloadPath + "*" + fileExtension)
            if currentFiles:
                # Sort the files by modification time (most recent first)
                currentFiles.sort(key=os.path.getmtime, reverse=True)

                # Get the most recently modified file
                currentFile = currentFiles[0]
                
                cutcurrentFile = currentFile.split('.')[0]
                # Remove only the first occurrence of the substring
                modified_current_file = cutcurrentFile + ".xls"
                os.rename(currentFile, modified_current_file)

                print("Recently downloaded file:", modified_current_file)
            else:
                print("No .xlsx files found in the directory.")
            got_file = True

        except IndexError:
            install_status = False
            print("File has not finished downloading")
            # interupt += 1
            time.sleep(7)
            return install_status

    # Create new file name
    fileDestination = os.path.join(downloadPath, newFileName + ".xls")

    # Check if the destination file already exists
    counter = 1
    while os.path.exists(fileDestination):
        # If it exists, append a counter to the file name
        newFileName_with_counter = f"{newFileName} ({counter})"
        fileDestination = os.path.join(
            downloadPath, newFileName_with_counter + ".xls")
        counter += 1

    # Create the target directory if it doesn't exist
    os.makedirs(os.path.dirname(fileDestination), exist_ok=True)
    os.rename(modified_current_file, fileDestination)
    time.sleep(5)
    print("rename: " + fileDestination)
    return install_status


def write_to_file(data_list, file_path, mode='w'):
    """
    Write a list of strings to a file.

    Parameters:
    - file_path (str): The path to the file.
    - data_list (list): The list of strings to be written to the file.
    - mode (str): The file mode ('w' for write, 'a' for append, etc.).

    Note: The default mode is 'w' (write).

    Example:
    write_list_to_file('output.txt', ['item1', 'item2', 'item3'])
    """
    directory = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)

    if data_list is not None:
        index_list = []
        for chat in data_list:
            index_list.append(take_index(chat))
        df = pd.DataFrame({"index": index_list, "chat": data_list})
        df.to_json(file_path, orient='records')
        # with open(file_path, mode=mode) as file:
        #     for item in data_list:
        #         file.write(f"{item}, ")
    else:
        print(f"No data {data_list} to write to file.")


def solve_captcha(driver):
    captcha = input("Press Enter to continue after solving the CAPTCHA...")
    captcha_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "txtSecurityCode")))
    captcha_element.send_keys(captcha)
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@id="btnmacDown" and contains(@class, "btn-login submit")]')))
    button.click()
    print("Continuing with the automation...")
    time.sleep(2.5)
    # data_selection

def download_file(driver, chat, start_date, end_date, download_directory):
    driver.find_element(By.ID, "btnDownload").click()
    time.sleep(2.5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@id="btnDownloadLocal"]'))).click()
    time.sleep(7)
    file_name = f"{take_index(chat)}. {chat.title()} {start_date} {end_date}"
    install_status = move_to_download_folder(download_directory + "/", file_name, ".xls")
    return install_status


INITIAL_START_DATE = date(1996, 12, 11)
INITIAL_END_DATE = date(1996, 12, 11)
CURRENT_START_DATE = date(1996, 12, 11)
def take_initial_end_date(start_date, end_date):
    global INITIAL_END_DATE
    INITIAL_END_DATE = end_date
    global INITIAL_START_DATE
    INITIAL_START_DATE = start_date
    global total_num_days
    total_num_days = (INITIAL_END_DATE - INITIAL_START_DATE).days


def find_input_date(driver, chat, start_date, end_date, download_directory, product_input, start_date_input, end_date_input):
    product_input.clear()
    start_date_input.clear()
    end_date_input.clear()
    product_input.send_keys(chat)
    start_date_input.send_keys(start_date.strftime("%Y-%m-%d"))
    end_date_input.send_keys(end_date.strftime("%Y-%m-%d"))
    driver.find_element(By.ID, "btnSubmit").click()
    time.sleep(3.5)
    transactions = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//span[contains(@data-bind, "text: viewModels.summary().frequency")]'))).text.strip()
    transactions = int(transactions)
    if start_date == INITIAL_START_DATE and end_date == INITIAL_END_DATE:
        global day_speed
        day_speed = transactions/total_num_days if total_num_days != 0 else 20
        print("total number of transactions: ", transactions)
    print("the remaining number of trans: ", transactions)

    while transactions > 500:
        times = transactions/500
        end_date_input.clear()
        
        num_of_days_found = floor((1/times)*(end_date - start_date).days)
        end_date = start_date + timedelta(days=num_of_days_found)
        
        end_date_input.send_keys(end_date.strftime("%Y-%m-%d"))
        
        driver.find_element(By.ID, "btnSubmit").click()
        time.sleep(3.5)
        transactions = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//span[contains(@data-bind, "text: viewModels.summary().frequency")]'))).text.strip()
        transactions = int(transactions)
        print(f"the current num of trans: {transactions}: {end_date.strftime('%Y-%m-%d')}")

        while transactions < 500-1.5*(day_speed) and end_date != INITIAL_END_DATE:
            time_step = floor((500-transactions)/day_speed)-3
            if time_step<=0:
                time_step=1
            end_date += timedelta(days=time_step)
            end_date_input.clear()

            end_date_input.send_keys(end_date.strftime("%Y-%m-%d"))
            driver.find_element(By.ID, "btnSubmit").click()
            time.sleep(3.5)
            transactions = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//span[contains(@data-bind, "text: viewModels.summary().frequency")]'))).text.strip()
            transactions = int(transactions)
            print(f"the current num of trans: {transactions}: {end_date.strftime('%Y-%m-%d')}")
            if transactions > 500:
                end_date -= timedelta(days=time_step)
                end_date_input.clear()

                end_date_input.send_keys(end_date.strftime("%Y-%m-%d"))
                driver.find_element(By.ID, "btnSubmit").click()
                time.sleep(3.5)
                transactions = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//span[contains(@data-bind, "text: viewModels.summary().frequency")]'))).text.strip()
                transactions = int(transactions)
                print(f"the current num of trans: {transactions}: {end_date.strftime('%Y-%m-%d')}")
                break

    global CURRENT_START_DATE
    CURRENT_START_DATE = start_date
    print(f"THE FINAL NUM OF TRANS IS: {transactions} for {start_date.strftime('%Y-%m-%d')} {end_date.strftime('%Y-%m-%d')}")
    if 0 < transactions <= 500:
        install_status = download_file(driver, chat, start_date, end_date, download_directory)
        if install_status ==True:
            return end_date
        else:
            return start_date-timedelta(days=1)
    else:
        print("something wrong")
        return None


def process_chat(driver, chat, start_date, end_date, download_directory, product_input, start_date_input, end_date_input):
    end_date_found = find_input_date(driver, chat, start_date, end_date, download_directory, product_input, start_date_input, end_date_input)
    if end_date_found == end_date:
        return True
    else:
        start_date_new = end_date_found + timedelta(days=1)
        return process_chat(driver, chat, start_date_new, end_date, download_directory, product_input, start_date_input, end_date_input)


def get_current_start_date():
    return CURRENT_START_DATE


def convert_x2x(downloadPath):
    got_file = False
    found_status = True  # file is not downloaded so nothing has been found
    # Grab current file name.
    # interupt=1
    while not got_file:
        try:
            currentFiles = glob.glob(downloadPath + "*.xls")
            got_file = True

        except IndexError:
            found_status = False
            print("File has not finished downloading")
            # interupt += 1
            time.sleep(5)
            return found_status

    for xls_file in currentFiles:
        # Extract the base filename (without extension)
        base_filename = os.path.splitext(os.path.basename(xls_file))[0]

        # Create the corresponding .xlsx filename
        xlsx_file = os.path.join(downloadPath, base_filename + ".xlsx")

        # Check if the destination file already exists
        # counter = 1
        # while os.path.exists(xlsx_file):
        #     # If it exists, append a counter to the file name
        #     newFileName_with_counter = f"{base_filename} ({counter})"
        #     xlsx_file = os.path.join(downloadPath, newFileName_with_counter + ".xlsx")
        #     counter += 1
        if os.path.exists(xlsx_file):
            continue

        # Convert .xls to .xlsx
        x2x = XLS2XLSX(xls_file)
        x2x.to_xlsx(xlsx_file)

        print(f"Converted \"{xls_file}\" to \"{xlsx_file}\"")
    return found_status