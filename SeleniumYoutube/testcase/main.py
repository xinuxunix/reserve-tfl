# https://selenium-python.readthedocs.io/page-objects.html#test-case
# https://www.youtube.com/watch?v=O_sIPPA4euw&list=PLzMcBGfZo4-n40rB1XaJ0ak1bemvlqumQ&index=6
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service # as a best of practice, use as a Service
from webdriver_manager.chrome import ChromeDriverManager

import page

class PythonOrgSearch(unittest.TestCase):

    # setUp and tearDown will be called every time when each single test being ran
    def setUp(self):
        print("setup")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) 
        self.driver.get('https://www.python.org')

    # def test_example(self):
    #     print("Test1 starts with test_")
    #     assert True

    # def test_example_2(self):
    #     print("Test2 starts with test_")
    #     assert False

    # def test_title(self):
    #     mainPage = page.MainPage(self.driver)
    #     assert mainPage.is_title_matches()

    def test_search_python(self):
        mainPage = page.MainPage(self.driver)
        assert mainPage.is_title_matches()
        mainPage.search_text_element = "pycon"
        mainPage.click_go_button()
        search_result_page = page.SearchResultsPage(self.driver)
        assert search_result_page.is_results_found()

    def tearDown(self):
        print("teardown")
        self.driver.close()

# The code snippet you provided is a common construct in Python scripts that checks if the script is being run 
# as the main program (as opposed to being imported as a module). If the script is run as the main program, the 
# code inside the if block will be executed.

# __name__ is a built-in variable in Python that represents the name of the current module. When a script is run 
# as the main program, the __name__ variable is set to "__main__". If the script is imported as a module in another 
# script, the __name__ variable will be set to the name of the module (i.e., the name of the file without the .py extension).

# In the code snippet provided, the unittest.main() function is called if the script is being run as the main program. 
# unittest.main() is part of Python's built-in unittest framework, which is used to run unit tests. When called, 
# it discovers and runs all the test methods in the script. By placing this function call inside the if 
# __name__ == "__main__": block, you ensure that the unit tests are only run when the script is executed as the main 
# program and not when it's imported as a module in another script.
if __name__ == "__main__": 
    unittest.main()