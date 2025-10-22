"""
Test script to verify Selenium installation
Run this first to make sure everything is set up correctly
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def test_selenium():
    print("Testing Selenium setup...")
    
    try:
        # This will automatically download the correct ChromeDriver
        print("Downloading ChromeDriver (one-time setup)...")
        service = Service(ChromeDriverManager().install())
        
        print("Starting Chrome browser...")
        driver = webdriver.Chrome(service=service)
        
        print("✓ Opening Google...")
        driver.get("https://www.google.com")
        
        print(f"✓ Page title: {driver.title}")
        print("\n✅ SUCCESS! Selenium is working correctly.")
        print("The browser will close in 5 seconds...")
        
        import time
        time.sleep(5)
        driver.quit()
        
        print("\nYou're ready to use the Teams deletion script!")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Chrome browser is installed")
        print("2. Try: pip install --upgrade selenium webdriver-manager")
        print("3. Restart your terminal/command prompt")

if __name__ == "__main__":
    test_selenium()
