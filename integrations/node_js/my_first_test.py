from seleniumbase import BaseCase
from selenium.webdriver.common.by import By
import string
import random


class MyTestClass(BaseCase):
    # Test method to be run for asserting account creation functionality +ve
    def test_signup(self):
        self.driver.delete_all_cookies()        # using delete cookies to avoid autopopulated values and stability
        self.open('https://www.simscale.com/')      # open application
        self.click_xpath("//a[@class='btn btn-primary btn-sign-up']")       # click the signup button
        self.click_xpath("//div[@id='msf-title']//button[@type='button']")      # click dropdown
        self.click_xpath("//div[@id='msf-title']//ul[@class='dropdown-menu']//li//a[@href='#'][contains(text(),'Mr.')]")    # select value Mr
        self.update_text("//input[@id='msf-first-name']", textgenerator(20))    # enter random text as first name
        self.update_text("//input[@id='msf-last-name']", textgenerator(20))     # enter random text as last name
        self.update_text("//input[@id='msf-email']", emailgenerator(20))        # enter randon email id
        self.update_text("//input[@id='msf-phone']", '+49 15160074857')     # enter phone number with country code
        password = ''.join(textgenerator(33))       # create a common password string for enter and confirm password screens
        self.update_text("//input[@id='msf-password']", password)       # enter password
        self.update_text("//input[@id='msf-confirm-password']", password)       # enter password
        self.click_xpath("//input[@id='msf-privacy-policy-confirmation']")      # checkbox select
        self.click_xpath("//input[@id='msf-news-and-updates']")     # checkbox select
        # assert if confirmation message for user created appears
        self.assert_element_present("//div[@class='main-signup-form-inner']"
                                    "//a[@class='btn btn-primary btn-close-progressinfo'][contains(text(),'Ok')]", 30)
        # click OK on confirmation message
        self.click_xpath("//button[@class='btn btn-primary btn-msf-submit']")

    # Test method to be run for checking session based login functionality with cookies enabled +ve
    def test_login(self):
        self.open('https://www.simscale.com/')  # Open application URL
        self.click_xpath("//a[@class='btn btn-default'][contains(text(),'Log in')]")    # click on login button
        self.assert_element_present("//img[@src='/assets/community/img/logo.png']")     # assert if logo is present
        self.assert_equal(self.driver.title, "SimScale Login", "page title is not correct")    # assert login page title
        # Should ideally use security framework for storing credentials for tests
        self.update_text("//input[@id='emailInput']", "Adityasarin3@gmail.com")     # enter user ID
        self.update_text("//input[@id='passInput']", "Rollo@1928")      # enter password
        self.click_xpath("//button[@id='authClick']")       # click login button
        self.assert_element_present("//div[@class='col-md-8']", 30)     # assert user specific icon set
        self.open("https://www.simscale.com/authentication/?action=logout")     # logout
        self.assert_equal(self.driver.title, "SimScale Login", "page title is not correct")     # assert if user is on the login page again
        self.go_back()      # click the browser back button
        self.assert_element_present("//button[@id='authClick']")        # assert if login button is present even after going back
        self.assert_equal(self.driver.title, "SimScale Login", "page title is not correct")    # assert page title
        self.refresh()      # refresh this page
        self.assert_equal(self.driver.title, "SimScale Login", "page title is not correct")     #check if user still is on the login page

    # Test method to e run for checking new project creation
    def test_createnewproject(self):
        self.open('https://www.simscale.com/')  # Open application URL
        self.click_xpath("//a[@class='btn btn-default'][contains(text(),'Log in')]")  # click on login button
        self.assert_element_present("//img[@src='/assets/community/img/logo.png']")  # assert if logo is present
        self.assert_equal(self.driver.title, "SimScale Login", "page title is not correct")  # assert login page title
        # Should ideally use security framework for storing credentials for tests
        self.update_text("//input[@id='emailInput']", "Adityasarin3@gmail.com")  # enter user ID
        self.update_text("//input[@id='passInput']", "Rollo@1928")  # enter password
        self.click_xpath("//button[@id='authClick']")  # click login button
        self.assert_element_present("//div[@class='col-md-8']", 30)  # assert user specific icon set
        self.click_xpath("//nav[@class='main-menu hidden-xs hidden-sm visible-md visible-lg']//a[contains(text(),'Dashboard')]")    # click on dashboard section in top menu
        self.scroll_to("//button[@id='newProject']", By.XPATH, 10)      # scroll to newproject button
        self.click_xpath("//button[@id='newProject']")      # click the button
        self.click_xpath("//input[@id='projectTitle']")     # click the title field
        self.update_text("//input[@id='projectTitle']", textgenerator(3))       # enter text less than 5 characters to check if error message is triggered
        self.click_xpath("//textarea[@id='projectDescription']")
        self.assert_element_visible("//span[contains(text(),'Project title must be at least 5 characters long')]", By.XPATH)        # assert if error message is shown
        self.click_xpath("//input[@id='projectTitle']")     # reenter valid title
        self.update_text("//input[@id='projectTitle']", textgenerator(3) + ' ' + textgenerator(2))
        self.assert_element_not_visible("//span[contains(text(),'Project title must be at least 5 characters long')]", By.XPATH)        # assert if error message is no longer shown with 6 character input
        self.click_xpath("//textarea[@id='projectDescription']")        # enter description now same as title
        self.update_text("//textarea[@id='projectDescription']", textgenerator(2))      # again repeat the validation for error message
        self.click_xpath("//div[@id='projectCategory']//div[@class='selectValue']")     # click on the dropdown now
        self.assert_element_visible("//span[contains(text(),'Description must be at least 5 characters long for')]")    # assert error message
        self.click_xpath("//textarea[@id='projectDescription']")        # enter correct length text
        self.update_text("//textarea[@id='projectDescription']", textgenerator(3) + ' ' + textgenerator(2))
        self.click_xpath("//div[@id='projectCategory']//div[@class='selectValue']")     # click category again to check if error message is not shown
        self.assert_element_not_visible("//span[contains(text(),'Description must be at least 5 characters long for')]")
        self.click_xpath("//div[@id='projectCategory']//div[@class='selectOptions']//div[1]")       # select first value
        self.assert_element_visible("//label[@for='project-visibility']", By.XPATH)     # assert feature to make projects private
        self.click_xpath("//span[@class='tagify__input']")       # enter tags
        self.update_text("//span[@class='tagify__input']", "aut\t")
        self.assert_element_not_visible("//span[contains(@class,'inputGroup__error projectTagsError')]", By.XPATH)
        self.click_xpath("//h5[contains(@class,'collapseTitle collapsed')]")    # check if advanced settings section is available
        self.assert_element_visible("//div[@id='measurements']//div[contains(@class,'selectValue')]", By.XPATH)
        self.assert_element_visible("//div[contains(@class,'dropzone-inner')]")
        self.click_xpath("//button[contains(@class,'btn btn-medium btn-primary btn-create-new-project inputSubmit')]")  # click on create button
        self.wait_for_element("//div[@class='ss-dropzone alert text-center']", 20)      # wait for new project screen to open
        self.open("https://www.simscale.com/authentication/?action=logout")     # logout
        # fin

def textgenerator(size=30, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def emailgenerator(size=30, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))+"@gmail.com"
