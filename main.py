from bs4 import BeautifulSoup  # Importing BeautifulSoup for parsing HTML
import lxml  # Importing lxml for parsing (not used directly in this code)
import requests  # Importing requests to make HTTP requests
from selenium import webdriver  # Importing Selenium WebDriver for browser automation
from selenium.webdriver.common.by import By  # Importing By for locating elements
import time  # Importing time for adding delays

# Define the URLs for the Zillow clone site and the Google Form
SITE_URL = "https://appbrewery.github.io/Zillow-Clone/"
FORM_URL = ("https://docs.google.com/forms/d/e/1FAIpQLSdWKtAzjxUt4Fh1YnEpbQ9_UikcrNG1b5zve_ZPmGVYUfgcww/viewform?"
            "usp=sf_link")

# Request the content\ of the Zillow Clone site
response = requests.get(SITE_URL)
content = response.text

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(content, "html.parser")

# Select property links from the parsed content
properties = soup.select(".StyledPropertyCardDataWrapper a")
link_list = []  # List to store property links
address_list = []  # List to store property addresses
price_list = []  # List to store property prices

# Loop through each property link to extract addresses and links
for link in properties:
    address_list.append(link.text.strip().replace("\n", "").replace("|", "").strip())  # Clean and store address
    link_list.append(link["href"])  # Store the property link

# Print the lists for debugging purposes
print(link_list)
print(address_list)

# Select price elements from the parsed content
cost = soup.select('span[data-test="property-card-price"]')
for amount in cost:
    price_list.append(amount.text.split("+")[0].split("/")[0])  # Clean and store prices

# Loop through the collected data and submit it to the Google Form
for n in range(len(link_list)):
    driver = webdriver.Chrome()  # Initialize the Chrome WebDriver
    driver.get(FORM_URL)  # Open the Google Form URL
    time.sleep(3)  # Wait for the page to load

    # Locate the input fields on the form
    input_form = driver.find_elements(By.CSS_SELECTOR, '.Xb9hP input[type="text"]')
    address_input = input_form[0]  # Address input field
    price_input = input_form[1]     # Price input field
    link_input = input_form[2]      # Link input field

    # Locate the submit button
    submit_button = driver.find_element(By.CSS_SELECTOR, '.lRwqcd div[aria-label="Submit"]')

    # Fill the form with scraped data
    address_input.send_keys(address_list[n])  # Enter address
    price_input.send_keys(price_list[n])      # Enter price
    link_input.send_keys(link_list[n])        # Enter link
    time.sleep(3)  # Wait before submitting

    # Click the submit button
    submit_button.click()

# Note: It's advisable to close the WebDriver after use
