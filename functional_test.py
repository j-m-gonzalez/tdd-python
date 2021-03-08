from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        #Willy checks out homepage
        self.browser.get('http://localhost:8000')

        #Willy sees the title and header
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        #Invited to enter to-do
        #Save to-do
        #Sees new to-do
        #Sees another prompt to enter to-do

if __name__ == '__main__':
    unittest.main()
