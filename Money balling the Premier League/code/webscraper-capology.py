from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, ElementClickInterceptedException
import pandas as pd
from ScraperFC.shared_functions import get_source_comp_info, InvalidCurrencyException

class Capology:

    def __init__(self, timeout=30):
        options = Options()
        options.add_argument('--headless')
        prefs = {'profile.managed_default_content_settings.images': 2}  # don't load images
        options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(options=options)
        self.timeout = timeout

        self.leagues = {
            'Bundesliga': 'de/1-bundesliga',
            '2.Bundesliga': '/de/2-bundesliga',
            'EPL': 'uk/premier-league',
            'EFL Championship': '/uk/championship',
            'Serie A': 'it/serie-a',
            'Serie B': 'it/serie-b',
            'La Liga': 'es/la-liga',
            'La Liga 2': 'es/la-liga-2',
            'Ligue 1': 'fr/ligue-1',
            'Ligue 2': 'fr/ligue-2',
            'Eredivisie': '/ne/eredivisie',
            'Primeira Liga': '/pt/primeira-liga',
            'Scottish PL': '/uk/scottish-premiership',
            'Super Lig': '/tr/super-lig',
            'Belgian 1st Division': 'be/first-division-a'
        }

        self.valid_currencies = ['eur', 'gbp', 'usd']

    def close(self):
        """ Closes and quits the Selenium WebDriver instance. """
        self.driver.close()
        self.driver.quit()

    def scrape_salaries(self, year, league, currency):
        """ Scrapes player salaries for the given league season. """
        _ = get_source_comp_info(year, league, 'Capology')
        if currency not in self.valid_currencies:
            raise InvalidCurrencyException()

        league_url = f'https://www.capology.com/{self.leagues[league]}/salaries/{year-1}-{year}'
        self.driver.get(league_url)

        # Show all players on one page
        done = False
        while not done:
            try:
                all_btn = WebDriverWait(
                    self.driver,
                    self.timeout,
                ).until(EC.element_to_be_clickable(
                    (By.LINK_TEXT, 'All')
                ))
                self.driver.execute_script("arguments[0].scrollIntoView(true);", all_btn)
                all_btn.click()
                done = True
            except StaleElementReferenceException:
                pass
            except ElementClickInterceptedException:
                # Handle overlapping elements, such as ads
                self.driver.execute_script("arguments[0].scrollIntoView(true);", all_btn)
                self.driver.execute_script("arguments[0].click();", all_btn)
            except TimeoutException:
                print("TimeoutException: 'All' button not clickable.")
                self.driver.save_screenshot('timeout_all_button.png')
                raise

        # Select the currency
        try:
            currency_btn = WebDriverWait(
                self.driver,
                self.timeout,
            ).until(EC.element_to_be_clickable(
                (By.ID, 'btn_{}'.format(currency))
            ))
            self.driver.execute_script('arguments[0].click()', currency_btn)
            print('Changed currency')
        except TimeoutException:
            print("TimeoutException: Currency button not clickable.")
            self.driver.save_screenshot('timeout_currency_button.png')
            raise

        # Table to pandas df
        try:
            tbody_html = self.driver.find_element(By.ID, 'table')\
                .find_element(By.TAG_NAME, 'tbody')\
                .get_attribute('outerHTML')
            table_html = '<table>' + tbody_html + '</table>'
            df = pd.read_html(table_html)[0]
            if df.shape[1] == 13:
                df = df.drop(columns=[1])
                df.columns = [
                    'Player', 'Weekly Gross', 'Annual Gross', 'Expiration', 'Length',
                    'Total Gross', 'Status', 'Pos. group', 'Pos.', 'Age', 'Country',
                    'Club'
                ]
            else:
                df.columns = [
                    'Player', 'Weekly Gross', 'Annual Gross', 'Adj. Gross', 'Pos. group',
                    'Age', 'Country', 'Club'
                ]
            return df
        except TimeoutException:
            print("TimeoutException: Table not found or loaded.")
            self.driver.save_screenshot('timeout_table.png')
            raise

# Example usage:
capology_instance = Capology(timeout=30)
try:
    salaries_data = capology_instance.scrape_salaries(2024, "EPL", "eur")
    print(salaries_data)
except TimeoutException as e:
    print("TimeoutException: ", e)
finally:
    capology_instance.close()
