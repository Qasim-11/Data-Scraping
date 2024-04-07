# This will scrap data from https://www.iau.edu.sa/ar/colleges/college-of-computer-science-and-information-technology/programs/bachelor-of-science-in-artificial-intelligence-0
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from find_next_urls import find_direct_child_paths
import pandas as pd
# URL
base_url = 'https://www.iau.edu.sa/ar/colleges/college-of-computer-science-and-information-technology'



def get_course_details(url , saved_file_name='data.csv'):
    # Send request
    response = requests.get(url)

    # Parse HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the tables
    tables = soup.find_all('table')

    # Extract the data
    data = []
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])

    # Create a DataFrame
    df = pd.DataFrame(data, columns=['Course Code', 'Course Title', 'Credit Hours', 'Prerequisites'])

    # Clean the data
    df['Course Code'] = df['Course Code'].str.replace('\n', '')
    df['Course Title'] = df['Course Title'].str.replace('\n', '')
    df['Credit Hours'] = df['Credit Hours'].str.replace('\n', '')
    df['Prerequisites'] = df['Prerequisites'].str.replace('\n', '')

    # Save the data
    df.to_csv(saved_file_name, index=False)
    print('Data saved to {saved_file_name}.csv')


majors = ["https://www.iau.edu.sa/ar/colleges/college-of-computer-science-and-information-technology/programs/bachelor-of-science-in-computer-science-cs" , "https://www.iau.edu.sa/ar/colleges/college-of-computer-science-and-information-technology/programs/bachelor-of-science-in-computer-information-systems-cis", "https://www.iau.edu.sa/ar/colleges/college-of-computer-science-and-information-technology/bachelor-of-science-in-cyber-security-and-digital-forensics-cys", "https://www.iau.edu.sa/ar/colleges/college-of-computer-science-and-information-technology/programs/bachelor-of-science-in-artificial-intelligence-0"]
for major in majors:
    # Split the URL by '/'
    parts = major.split('/')
    # Find the index of 'programs' or the default to the last segment if 'programs' is not found
    index = parts.index('programs') + 1 if 'programs' in parts else -1
    major_name = parts[index] if index != -1 else parts[-1]
    get_course_details(major, f'{major_name}.csv')