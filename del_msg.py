"""
Microsoft Teams Message Deletion via Browser Automation

SETUP:
1. Install: pip install selenium webdriver-manager
2. Make sure Chrome browser is installed
3. Run the script
4. Login manually when browser opens
5. Let it run!

IMPORTANT: This only deletes YOUR messages (Teams restriction)
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

class TeamsMessageDeleter:
    def __init__(self, headless=False):
        """Initialize the browser"""
        print("Initializing browser...")
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        # Keep your Teams session logged in
        options.add_argument('--user-data-dir=./teams_profile')
        
        if headless:
            options.add_argument('--headless')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 20)
        
    def login_to_teams(self):
        """Navigate to Teams and wait for manual login"""
        print("Opening Teams...")
        self.driver.get("https://teams.microsoft.com")
        
        print("\n⚠️  Please log in manually in the browser window")
        print("Once logged in and you can see your chats, press ENTER here...")
        input()
        print("Continuing with automation...")
        time.sleep(3)
    
    def navigate_to_chat(self, chat_name):
        """Navigate to a specific chat by name"""
        print(f"Searching for chat: {chat_name}")
        
        try:
            # Click on search box
            search_box = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[placeholder='Search']"))
            )
            search_box.click()
            search_box.send_keys(chat_name)
            time.sleep(2)
            
            # Click first result
            first_result = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[role='option']"))
            )
            first_result.click()
            time.sleep(2)
            print(f"✓ Opened chat: {chat_name}")
            
        except Exception as e:
            print(f"Error navigating to chat: {e}")
            raise
    
    def delete_messages(self, count=10, delay=1):
        """
        Delete messages by hovering and clicking delete
        
        Args:
            count: Number of messages to delete (set high for all)
            delay: Delay between deletions in seconds
        """
        deleted = 0
        attempts = 0
        max_attempts = count * 3  # In case some messages can't be deleted
        
        print(f"\nStarting deletion process (targeting {count} messages)...")
        
        while deleted < count and attempts < max_attempts:
            attempts += 1
            
            try:
                # Find all message containers
                # Note: Selectors may need adjustment based on Teams updates
                messages = self.driver.find_elements(
                    By.CSS_SELECTOR, 
                    "[data-tid='message-body-content']"
                )
                
                if not messages:
                    print("No more messages found")
                    break
                
                # Work backwards (delete newest first)
                for msg in reversed(messages[-5:]):  # Process last 5 messages
                    try:
                        # Scroll message into view
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView(true);", 
                            msg
                        )
                        time.sleep(0.5)
                        
                        # Hover over message to reveal more options
                        ActionChains(self.driver).move_to_element(msg).perform()
                        time.sleep(0.5)
                        
                        # Look for "More options" button (three dots)
                        more_options = msg.find_element(
                            By.CSS_SELECTOR,
                            "[data-tid='message-more-options'], [aria-label*='More options']"
                        )
                        more_options.click()
                        time.sleep(0.5)
                        
                        # Click "Delete" option
                        delete_button = self.wait.until(
                            EC.element_to_be_clickable((
                                By.XPATH,
                                "//button[contains(., 'Delete') or contains(@aria-label, 'Delete')]"
                            ))
                        )
                        delete_button.click()
                        time.sleep(0.5)
                        
                        # Confirm deletion if dialog appears
                        try:
                            confirm = self.driver.find_element(
                                By.XPATH,
                                "//button[contains(., 'Delete') or contains(@aria-label, 'Delete')]"
                            )
                            confirm.click()
                            time.sleep(0.3)
                        except:
                            pass  # No confirmation dialog
                        
                        deleted += 1
                        print(f"✓ Deleted message {deleted}/{count}")
                        time.sleep(delay)
                        
                        if deleted >= count:
                            break
                            
                    except Exception as e:
                        # Message might not be deletable (not yours, etc.)
                        print(f"⊘ Skipped a message: {str(e)[:50]}")
                        continue
                
                # Scroll up to load older messages
                self.driver.execute_script("window.scrollBy(0, -500);")
                time.sleep(1)
                
            except Exception as e:
                print(f"Error in deletion loop: {e}")
                time.sleep(2)
        
        print(f"\n✓ Deletion complete! Deleted {deleted} messages")
    
    def delete_all_in_chat(self, chat_name, max_messages=1000, delay=1):
        """
        Delete all your messages in a specific chat
        
        Args:
            chat_name: Name of the chat/person
            max_messages: Safety limit (set lower for testing)
            delay: Delay between deletions
        """
        self.navigate_to_chat(chat_name)
        self.delete_messages(count=max_messages, delay=delay)
    
    def close(self):
        """Close the browser"""
        print("\nClosing browser...")
        self.driver.quit()

# Example usage
if __name__ == "__main__":
    deleter = TeamsMessageDeleter()
    
    try:
        # Step 1: Login
        deleter.login_to_teams()
        
        # Step 2: Delete messages
        # Option A: Navigate to specific chat and delete
        deleter.delete_all_in_chat(
            chat_name="John Doe",  # Replace with actual chat name
            max_messages=50,        # Start with low number for testing
            delay=1.5               # Delay between deletions
        )
        
        # Option B: If already in a chat, just delete
        # deleter.delete_messages(count=20, delay=1)
        
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        deleter.close()
