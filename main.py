from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

def example_com():
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")

    with webdriver.Firefox(options=options) as driver:
        driver.get("https://www.example.com")
        
        # first page content
        element = driver.find_element(By.XPATH, "/html/body/div/p[1]")
        print("Element 1 found:", element.text)
        
        # second page content
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > p:nth-child(3) > a:nth-child(1)").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".help-article > p:nth-child(2)")))
        element2 = driver.find_element(By.CSS_SELECTOR, ".help-article > p:nth-child(2)")
        print("Element 2 found:", element2.text)
        
        # third page content
        driver.find_element(By.CSS_SELECTOR, "#logo > a:nth-child(1) > img:nth-child(1)").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#intro > p:nth-child(1)")))
        element3 = driver.find_element(By.CSS_SELECTOR, "#intro > p:nth-child(1)")
        print("Element 3 found:", element3.text)
        
        # find search box and perform search
        from selenium.common.exceptions import NoSuchElementException
        try:
            search_box = driver.find_element(By.ID, "gsc-i-id1")
            search_box.send_keys("sample search")
            driver.find_element(By.CLASS_NAME, "gsc-search-button").click()
        except NoSuchElementException:
            print("Search box with ID 'gsc-i-id1' not found.")
            return
        
        # load search results
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "resInfo-0")))
            time_taken = driver.find_element(By.ID, "resInfo-0")
            print("Search result info:", time_taken.text)
        except Exception as e:
            print("Search result info element not found:", e)
        
        # parse the search results container with BeautifulSoup
        results_container = driver.find_element(By.CLASS_NAME, "gsc-resultsbox-visible")
        soup = BeautifulSoup(results_container.get_attribute('innerHTML'), 'html.parser')
        results = soup.find_all(class_='gsc-webResult gsc-result')
        print("Search Results:")
        for result in results:
            title = result.find(class_='gs-title')
            if title is not None:
                print(title.get_text())

def tab_switching():
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")

    with webdriver.Firefox(options=options) as driver:
        driver.get("https://www.example.com")
        main_handle = driver.current_window_handle

        # open second tab
        driver.execute_script("window.open('https://github.com/mpvio', 'second')")
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        driver.switch_to.window("second")
        second_handle = driver.current_window_handle
        print(f"Current window handle: {second_handle}")

        # get info from second tab
        repository_count = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/main/div[1]/div/div/div[2]/div/nav/a[2]/span").text
        repo_word = "repository" if repository_count == 1 else "repositories"
        print(f"I have {repository_count} {repo_word}.")

        # switch back to first tab
        driver.close()
        driver.switch_to.window(main_handle)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div:nth-child(1) > h1:nth-child(1)")))
        element = driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > h1:nth-child(1)").text
        print(f"Current handle: {main_handle}. Current page: {element}.")


if __name__ == "__main__":
    example_com()
    tab_switching()