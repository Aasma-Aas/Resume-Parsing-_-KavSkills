import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from flask import Flask, render_template, request, redirect, url_for

class Profiles:
    def __init__(self, username, password, choice, target, location, options=None):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.username = username
        self.password = password
        self.choice = choice
        self.target = target
        self.location = location

    def login(self):
        self.driver.get('https://www.linkedin.com/login')
        username_field = self.driver.find_element(By.ID, 'username')
        password_field = self.driver.find_element(By.ID, 'password')
        login_button = self.driver.find_element(By.CLASS_NAME, 'btn__primary--large')
        username_field.send_keys(self.username)
        password_field.send_keys(self.password)
        login_button.click()

    def collect_links(self):
        # Create a folder named after the choice
        folder_name = self.choice.replace(" ", "_")
        os.makedirs(folder_name, exist_ok=True)

        profile_links = []
        target_links = int(self.target)
        page = 0
        while len(profile_links) < target_links:
            try:
                search_url = f"https://www.linkedin.com/search/results/people/?&keywords={self.choice}&origin=CLUSTER_EXPANSION&page={page + 1}"
                self.driver.get(search_url)
                
                # Handle location-related code with a try...except block
                try:
                    wait = WebDriverWait(self.driver, 10)
                    location_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[3]/div[2]/section/div/nav/div/ul/li[4]/div/span/button')))
                    location_btn.click()
                    input_field = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[3]/div[2]/section/div/nav/div/ul/li[4]/div/div/div/div[1]/div/form/fieldset/div[1]/div/div/input')))
                    input_field.send_keys(self.location)
                    loc_show = wait.until(EC.element_to_be_clickable((By.XPATH, '//html/body/div[5]/div[3]/div[2]/section/div/nav/div/ul/li[4]/div/div/div/div[1]/div/form/fieldset/div[2]/button[2]')))
                    loc_show.click()
                except Exception as e:
                    print("Location-related code failed, executing alternative code...")
                    # Place your alternative code here

                ul_element = self.driver.find_element(By.CLASS_NAME, 'reusable-search__entity-result-list')
                li_elements = ul_element.find_elements(By.TAG_NAME, 'li')

                collected_links = 0
                for li in li_elements:
                    try:
                        profile_link = li.find_element(By.TAG_NAME, "a")
                        profile_url = profile_link.get_attribute("href")
                        profile_links.append(profile_url)
                        collected_links += 1
                    except Exception as e:
                        print('Error: ', {str(e)})

                if collected_links == 0:
                    break
                page += 1
            except Exception as e:
                print(f"Exception in main loop: {str(e)}")


        df = pd.DataFrame(profile_links, columns=["ProfileLink"])
        # df.to_csv("linkedin_profiles.csv", index=False)

        wait = WebDriverWait(self.driver, 10)
        for profile_link in profile_links:
            self.driver.get(profile_link)
            try:
                save_to_pdf_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]/button')))
                save_to_pdf_button.click()
                download_pdf_option = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[3]/div/div/div/2/div/div/main/section[1]/div[2]/div[3]/div/div[2]/div/div/ul/li[2]/div')))
                download_pdf_option.click()
                time.sleep(2)

                old_pdf_path = os.path.expanduser('~/Downloads/linkedin_profile.pdf')
                new_pdf_path = os.path.join(folder_name, f'profile_{len(profile_links)}_{int(time.time())}.pdf')
                os.rename(old_pdf_path, new_pdf_path)
            except Exception as e:
                print(f"Exception in PDF download: {str(e)}")
