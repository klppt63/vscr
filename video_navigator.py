import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def activechannels_ScrubTV():
    options = Options()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get("https://reboot.tube/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'table-bordered')))
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', {'class': 'table table-bordered table-striped'})
    if table is None:
        return "Table not found"
    rows = table.find_all('tr')
    channels = []
    for i, row in enumerate(rows[1:]):
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        link = row.find_all('a')[0]['href']
        channels.append({
            'Number': i + 1,
            'Channel': re.sub(r'\s*\(.*\)', '', cols[0]),
            'Now Playing': cols[2],
            'Link': link
        })
    driver.quit()

    max_length = 1900
    table_str = "```\n" + "| #  | Channel              | Now Playing               |\n" + "| -- | -------------------- | ------------------------- |\n"
    for channel in channels:
        line = f"| {channel['Number']:<2} | {channel['Channel'][:20].ljust(20)} | {channel['Now Playing'][:25].ljust(25)} |\n"
        if len(table_str) + len(line) > max_length:
            break
        table_str += line
    table_str += "```\n"
    return table_str

print(activechannels_ScrubTV())
