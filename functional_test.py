from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        #Willy checks out homepage
        self.browser.get('http://localhost:8000')

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
        time.sleep(1)
        self.check_for_row_in_list_table('1: Make fudge')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Eat fudge')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        #Page updates again, shows both items on list
        self.check_for_row_in_list_table('1: Make fudge')
        self.check_for_row_in_list_table('2: Eat fudge')
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Make fudge', [row.text for row in rows])
        self.assertIn('2: Eat Fudge', [row.text for row in rows])
        #Sees another prompt to enter to-do
        self.fail("Finish test!")
        # page updates again

if __name__ == '__main__':
    unittest.main()
