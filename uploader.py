import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
# import chromedriver_autoinstaller

# chromedriver_autoinstaller.install()


# Specify the folder path you want to iterate through
folder_path = '/Volumes/Non Apple/Scraper/essays/'

# Create a CSV file to store the results
csv_filename = 'humanity_scores.csv'
with open(csv_filename, 'w', newline='') as csvfile:
    fieldnames = ['file_name', 'humanity_score']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the CSV header
    writer.writeheader()

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the item is a file (not a subfolder)
        if os.path.isfile(os.path.join(folder_path, filename)):
            # Process the file here
            file_path = os.path.join(folder_path, filename)

            # Initialize the WebDriver
            service = webdriver.chrome.service.Service(executable_path='chromedriver-mac-x64/chromedriver')
            options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(service=service, options=options)

            # Open the hesiod.ca website
            driver.get('https://hesiod.ca/detector')

            # Execute JavaScript to enter full-screen mode
            # driver.execute_script("document.documentElement.webkitRequestFullscreen();")
            # pyautogui.hotkey('ctrl', 'cmd', 'f')

            # Find the file input element and upload a file
            file_input = driver.find_element(By.NAME, 'file_input')
            file_input.send_keys(file_path)

            # driver.execute_script("window.scrollBy(0, 400);")

            element = driver.find_element(By.XPATH, '/html/body/section/div[2]/main/div/div/form/button[1]')
            driver.execute_script("arguments[0].click();", element)

            # Wait for the loading spinner to disappear (maximum 20 seconds)
            wait = WebDriverWait(driver, 20)
            wait.until(EC.invisibility_of_element_located((By.XPATH, '//button[@id="loading-spinner"]')))

            # Find the humanity score element and extract its text
            humanity_score_element = driver.find_element(By.XPATH, '//h5[contains(text(), "Humanity Score:")]')
            humanity_score_text = humanity_score_element.text

            # Extract the numeric value from the text
            numeric_part = humanity_score_text.split(':')[1].strip()
            try:
                humanity_score_numeric = float(numeric_part)
            except ValueError:
                print("Error: Unable to convert numeric part to float:", numeric_part)
                humanity_score_numeric = None

            # Write the results to the CSV file
            writer.writerow({'file_name': filename, 'humanity_score': humanity_score_numeric})

            # Print the humanity score and decision
            if humanity_score_numeric is not None:
                print("File Name:", filename)
                print("Humanity Score Text:", humanity_score_text)
                print("Humanity Score Numeric:", humanity_score_numeric)

            # Close the browser
            driver.quit()
