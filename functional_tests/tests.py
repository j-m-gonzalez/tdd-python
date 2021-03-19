from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 5

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)


    def test_can_start_a_list_and_for_one_user(self):
        #Willy checks out homepage
        self.browser.get(self.live_server_url)

        #Willy sees the title and header
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #Invited to enter to-do
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        # Dude enters 'make fudge' in box to-do
        inputbox.send_keys('Make fudge')
        # Dude hits enter, page updates and now the list says
        # "1: Make fudge"
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Make fudge')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Eat fudge')
        inputbox.send_keys(Keys.ENTER)

        #Page updates again, shows both items on list
        self.wait_for_row_in_list_table('2: Eat fudge')
        self.wait_for_row_in_list_table('1: Make fudge')
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Make fudge', [row.text for row in rows])
        self.assertIn('2: Eat fudge', [row.text for row in rows])
        #Sees another prompt to enter to-do
        # page updates again

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # W starts new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Make fudge')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Make fudge')

        # He notices list has unique URL
        willy_list_url = self.browser.current_url
        self.assertRegex(willy_list_url, '/lists/.+')

        # New user, Hank comes
        ## new browser session for cookies
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Hank visits home page. None of W's lists
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Make fudge', page_text)
        self.assertNotIn('Eat fudge', page_text)

        # Hank starts new list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Hank gets a unique URL
        hank_list_url = self.browser.current_url
        self.assertRegex(hank_list_url, '/lists/.+')
        self.assertNotEqual(hank_list_url, willy_list_url)

        # None of Willy's list here
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy fudge', page_text)
        self.assertIn('Buy milk', page_text)
