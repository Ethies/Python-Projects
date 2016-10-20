# -*- Orange Testing Script ADDING AN USER -*-
# -*- coding: utf-8 -*-
'''
This code comprise below items:
 - Opening the URL
 - Login the site
 - Clicking the menu
 - Adding the New User
 - Searching the User name in the multiple pages
 - Editing and updating the User details
 - Verifying the Success Message after updating
 - Having 5 test cases
 - Note: update the 'U_NAME' value in variables file for adding new username
 
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import unittest
import time
import variables

class ExampleScript15(unittest.TestCase):
    
    #url = "https://enterprise-demo.orangehrmlive.com/auth/login"
     
    @classmethod
    def __init__(cls):
        super(ExampleScript15, cls).setUpClass()
        cls.driver = webdriver.Chrome()
        cls.driver.get(cls.url)
        cls.driver.implicitly_wait(30)
        cls.verificationErrors = []
          
    #Login the page
    def test_login_User(self):
       
        print("test_login_user start")
        self.driver.find_element_by_id("txtUsername").clear()
        self.driver.find_element_by_id("txtUsername").send_keys(variables.LOGIN_NAME)

        self.driver.find_element_by_id("txtPassword").clear()
        self.driver.find_element_by_id("txtPassword").send_keys(variables.PASSWORD)
        self.driver.find_element_by_id("btnLogin").click()

        print("test_login_user end")
          
    #Click the Admin Menu
    def test_to_Click_Admin_menu(self):
        print("test_to_click_admin_menu start")
        self.driver.find_element_by_xpath("//a[@id='menu_admin_viewAdminModule']/b").click()
        time.sleep(4)
        # Mouse the menu and selecting the sub menu
        menu = self.driver.find_element_by_xpath("//a[@id='menu_admin_UserManagement']")
        hidden_submenu = self.driver.find_element_by_xpath("//a[@id='menu_admin_viewSystemUsers']")
        actions = ActionChains(self.driver)
        actions.move_to_element(menu)
        actions.click(hidden_submenu)
        actions.perform()
        print("test_to_click_admin_menu end")
   
    #Add User from this page- Click the ADD button
    def test_to_Add_User(self):   
        print("test_to_add_user start")
        self.driver.find_element_by_id("btnAdd").click()
        self.driver.find_element_by_id("systemUser_essRole").click()
        self.driver.find_element_by_css_selector("option[value=\"2\"]").click()
        self.driver.find_element_by_id("systemUser_supervisorRole").click()
        self.driver.find_element_by_css_selector("option[value=\"3\"]").click()
        self.driver.find_element_by_id("systemUser_adminRole").click()
        #Select(self.driver.find_element_by_id("systemUser_adminRole")).select_by_visible_text("Finance Team")
        Select(self.driver.find_element_by_id("systemUser_adminRole")).select_by_visible_text("Global Admin")
        self.driver.find_element_by_id("systemUser_employeeName_empName").click()
        self.driver.find_element_by_id("systemUser_employeeName_empName").send_keys(variables.EMPLOYEE_NAME)
        self.driver.find_element_by_id("systemUser_userName").click()
        self.driver.find_element_by_id("systemUser_userName").clear()
        self.driver.find_element_by_id("systemUser_userName").send_keys(variables.U_NAME)
        self.driver.find_element_by_id("systemUser_status").click()
        self.driver.find_element_by_css_selector("#systemUser_status > option[value=\"1\"]").click()
        self.driver.find_element_by_id("systemUser_password").click()
        self.driver.find_element_by_id("systemUser_password").clear()
        self.driver.find_element_by_id("systemUser_password").send_keys(variables.P_WORD)
        self.driver.find_element_by_id("systemUser_confirmPassword").click()
        self.driver.find_element_by_id("systemUser_confirmPassword").clear()
        self.driver.find_element_by_id("systemUser_confirmPassword").send_keys(variables.CONFIRM_P_WORD)
        self.driver.find_element_by_id("UserHeading").click()
        self.driver.find_element_by_id("btnSave").click()
        
        #Verify the Username is added successfully
            
        try:
            #Check the success message
            print "check system displayed success message"
            Succ_add_msg = self.driver.find_element_by_xpath("//form[@id='frmList_ohrmListComponent']/div[2]").text
            print "The popup message on page is:", Succ_add_msg
            self.assertTrue("Successfully Saved Close", Succ_add_msg)
            print "The success message displayed :)"
           
            '''
            # For Financial option only - Check the All Region Checkbox status and Save
            
            checkbox = self.driver.find_element_by_name("userRegion[global]")       

            if (checkbox.is_selected()):
                print("Checkbox is already selected...")
            else:
                print("Checkbox is not selected..now selecting it")
                checkbox.click()    
           
            print "Click SAVE button"
            self.driver.find_element_by_id("btnSave").click()                   
            
            '''
            
        except NoSuchElementException as e:
                print ("Exception occurred in previous script", format(e));
            
                print "Already Username Exist message displayed"   
                
                user_name = self.driver.find_element_by_id("systemUser_userName-error")
                user_text = user_name.get_attribute('value')
                self.assertEqual(user_text,'Already exists')
                
                #Also can verify
                
                print "start assert equal"
                self.assertEqual("Already exists", self.body.text)
                
                print "ends assert equal"

    
                print "User name Already Exist." 
        
        print("test_to_add_user end")
     
    def test_search_the_added_user(self):
        # Search the User name in the site
        # USER_NAME - this variable is the user name required to search in the site
        
        print "test_Start user search"

        table_id = self.driver.find_element(By.TAG_NAME, "tbody")
        rows = table_id.find_elements(By.TAG_NAME, "tr")
        #col = rows[1].find_elements(By.TAG_NAME, "td")    
        
        while variables.Search_Update_USER_NAME != rows:
            table_id = self.driver.find_element(By.TAG_NAME, "tbody")   # Declaring again
            rows = table_id.find_elements(By.TAG_NAME, "tr")            # Declaring again
            
            for i in rows:
                col = i.find_elements(By.TAG_NAME, "td")[1]
                print (col.text)
               
                if variables.Search_Update_USER_NAME in col.text:
                    print "Username found"   
                    return variables.Search_Update_USER_NAME

            print "Not found in current page.. moving to next page"
            self.driver.find_element(By.XPATH, "(//a[contains(text(),'Next')])[2]").click() 
            print "on next page"
            time.sleep(5)
             
        print "test_Ends user search"
        
    def test_click_the_username(self):
        
        # Click the USer name and Update the details
        
        print "test_Start_click username"
               
        self.driver.find_element_by_link_text(variables.Search_Update_USER_NAME).click()
            
        # click the Edit button
        self.driver.find_element_by_id("btnSave").click()
        print "Clicked the Edit button"

            
        print "Verify Edit button changed to Save button"
        
        element = self.driver.find_element_by_id("btnSave")
        element_attribute = element.get_attribute("value").encode('utf8')      # this value is in unicode u'Save', so changing to str
        print "attr:", type(element_attribute)
        print "The button value is:", element_attribute
                       
        self.assertEqual("Save", element_attribute )

        # or --self.assertEqual("Save", self.driver.find_element_by_id("btnSave").get_attribute("value"))
        print "Both the texts are same"
        print "Page is in Edit mode"
        
        
        # Verify the Employee Name 
        print "verify the empl name"
        Emp_Name = self.driver.find_element_by_id("systemUser_employeeName_empName").get_attribute("value").encode('utf8')
        self.assertTrue(variables.EMPLOYEE_NAME, Emp_Name)
        print "The Emp Name in the form:", Emp_Name
        print "Both the Names are same"
        
        print "Verified Employee name"

        # Update the Employee name
        self.driver.find_element_by_id("systemUser_employeeName_empName").click()
        self.driver.find_element_by_id("systemUser_employeeName_empName").clear()
        self.driver.find_element_by_id("systemUser_employeeName_empName").send_keys(variables.EMPLOYEE_NAME)
        
        self.driver.find_element_by_id("btnSave").click()  
        
        print "Successfully updated"
        
        # Verify the update success message
        Succ_msg = self.driver.find_element_by_xpath("//form[@id='frmList_ohrmListComponent']/div[2]").text
        print "The popup message on page is:", Succ_msg
        self.assertTrue("Successfully Updated Close", Succ_msg)        
   
        #Get the screenshot on this page
        self.driver.save_screenshot('screenshot-firefox.jpg') 
        
        print "test_Ends_click username"             

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        
        except NoSuchElementException as e:
            print ("Exception occurred in previous script", format(e));        
    
    @classmethod
    def tearDownClass(cls):
        super(ExampleScript15, cls).tearDownClass()
        cls.driver.close()

    def suite(self):

        """ Gather all the tests from this module in a test suite. """
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(ExampleScript15))
        return suite
    
if __name__ == "__main__":
    # Run the Test Suite
    suiteFew = unittest.TestSuite()
    # Order of Execution of each methods
    suiteFew.addTest(ExampleScript15("test_login_User"))
    suiteFew.addTest(ExampleScript15("test_to_Click_Admin_menu"))
    suiteFew.addTest(ExampleScript15("test_to_Add_User"))
    suiteFew.addTest(ExampleScript15("test_search_the_added_user"))
    suiteFew.addTest(ExampleScript15("test_click_the_username"))
    unittest.TextTestRunner(verbosity=2).run(suiteFew)
    