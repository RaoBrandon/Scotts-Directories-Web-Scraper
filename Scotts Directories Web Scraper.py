import csv
import time
from selenium import webdriver
from timeit import default_timer as timer
from selenium.common.exceptions import StaleElementReferenceException


class Scraper:

    def __init__(self):
        """
        initialize our container variables and webdriver instance, we also need to open a new csv file and write the
        header to it
        """
        self.sorted_info = []
        self.tracked_parameters = ["Company:", "Scotts ID:", "Legal Name:", "# of Employees:", "Address:", "Sales:",
                                   "Square Footage:", "Telephone:", "Year Established:", "Head Office:",
                                   "Geocoded By:", "Fax:", "Web Site:", "Census Division:", "Executives:", "NAICS:",
                                   "Business Types:", "Products:", "Exporter (Y/N):", "Location Address:",
                                   "Parent Company:"]
        self.new_file = open('extract.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.new_file)
        self.csv_writer.writerow(self.tracked_parameters)
        # we initialize our driver with options, making it so that we open the chrome window in our signed in state
        options = webdriver.ChromeOptions()
        options.add_argument("user-data-dir=C:/Users/iamso/AppData/Local/Google/Chrome/User Data")
        self.browser = webdriver.Chrome(executable_path="C:/Users/iamso/Desktop/chromedriver", options=options)

    def search(self):
        """
        the purpose of this method is to go through the search parameters and make sure that we are searching for
        businesses within our target geographies, in this case we are considering Ontario and British Columbia
        """
        # opening website, signing in is unnecessary because we accessed chrome in signed in mode
        self.browser.get(
            'http://www.scottscanadianbusinessdirectory.com.ezproxy.torontopubliclibrary.ca/English/_Detail.aspx')
        time.sleep(0.5)
        # button to sign in
        button = self.browser.find_element_by_xpath('''//*[@id="signin-form"]/div[2]/dd/input''')
        button.click()
        time.sleep(0.5)
        # button to start a new search query
        button = self.browser.find_element_by_xpath('''//*[@id="ContentPlaceHolder1_Panel2"]/div[2]/p/a''')
        button.click()
        time.sleep(0.5)
        # button to search by city
        button = self.browser.find_element_by_xpath('''//*[@id="MenuVerticaln1"]/td/table/tbody/tr/td/a''')
        button.click()
        time.sleep(100)

    def press_button(self):
        """
        call this method to press the next record button and iterate through all records in the database
        """
        button = self.browser.find_element_by_xpath('''//*[@id="ContentPlaceHolder1_ibNext"]''')
        button.click()

    def get_info(self):
        """
        this method collects all of the tags associated with td and puts it into a sorted list form to be read by
        self.concatenate, which writes it to a CSV file
        """
        self.start = timer()
        to_skip = ["", " ", "Search Manager", "View Manager", "Preferences"]
        sorted_info = [data.text for data in self.browser.find_elements_by_tag_name('td') if
                       data.text not in to_skip]
        return sorted_info

    def concatenate(self, sorted_info):
        """
        this method takes the list sorted_info and puts it in a readable format with each business being 1 entry
        # in the list, it then writes that entry into a CSV file
        """
        readable_data = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
        index = 0
        for tag_number in range(0, len(sorted_info)):
            if sorted_info[tag_number] in self.tracked_parameters:
                current_tag = sorted_info[tag_number]
                if current_tag == "Company:":
                    index = 0
                elif current_tag == "Scotts ID:":
                    index = 1
                elif current_tag == "Legal Name:":
                    index = 2
                elif current_tag == "# of Employees:":
                    index = 3
                elif current_tag == "Address:":
                    index = 4
                elif current_tag == "Sales:":
                    index = 5
                elif current_tag == "Square Footage:":
                    index = 6
                elif current_tag == "Telephone:":
                    index = 7
                elif current_tag == "Year Established:":
                    index = 8
                elif current_tag == "Head Office:":
                    index = 9
                elif current_tag == "Geocoded By:":
                    index = 10
                elif current_tag == "Fax:":
                    index = 11
                elif current_tag == "Web Site:":
                    index = 12
                elif current_tag == "Census Division:":
                    index = 13
                elif current_tag == "Executives:":
                    index = 14
                elif current_tag == "NAICS:":
                    index = 15
                elif current_tag == "Business Types:":
                    index = 16
                elif current_tag == "Products:":
                    index = 17
                elif current_tag == "Exporter (Y/N):":
                    index = 18
                elif current_tag == "Location Address:":
                    index = 19
                elif current_tag == "Parent Company:":
                    index = 20
            else:
                if index in [3, 5, 6, 8, 10]:
                    if readable_data[index] == "":
                        readable_data[index] += sorted_info[tag_number]
                else:
                    readable_data[index] += sorted_info[tag_number]
        self.csv_writer.writerow(readable_data)
        self.end = timer()
        self.time_taken = self.end - self.start

    def quit(self):
        """
        All this does is make sure that the browser and CSV file are closed to prevent any errors from popping up
        once the program has finished executing
        """
        # close the browser instance and csv writer
        self.browser.quit()
        self.new_file.close()


# initialize our scraper object
scraper = Scraper()
# start the search process
scraper.search()

# for now, we want to look at a temporary amount of entries but we can have it custom depending on the amount of
# entries defined by the search method, for now we look at the entire 85000
for business_page in range(0, 95000):
    while True:
        try:
            scraper.concatenate(scraper.get_info())
            break
        except StaleElementReferenceException:
            time.sleep(0.1)
    time.sleep(scraper.time_taken)
    scraper.press_button()
# close the browser instance
scraper.quit()
