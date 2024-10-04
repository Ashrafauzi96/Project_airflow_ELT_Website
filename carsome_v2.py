import requests
from bs4 import BeautifulSoup
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

car_name = []
Car_Mileage = []
Car_Transmission = []
Car_Location = []
Car_Price = []
Car_Instalment_Monthly_Amount = []

def extract_data():
    global car_name
    global Car_Mileage
    global Car_Transmission 
    global Car_Location
    global Car_Price
    global Car_Instalment_Monthly_Amount 

    for i in range(1,6):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920x1080')
        
        driver = webdriver.Chrome(options=options)
        driver.get('https://www.carsome.my/buy-car?pageNo='+str(i))
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')

        #1. CAR NAME
        for element in soup.find_all(attrs={'class': 'mod-b-card__title'}):
            name = element.find('p')
            if name not in car_name:
                car_name.append(name.text)
        #remove new line
        car_name = [e.strip().replace('\n', '') for e in car_name if e != '']
        # Remove extra spaces
        car_name = [' '.join(item.split()) for item in car_name]

        #2. CAR MILEAGE
        for element_2 in soup.find_all(attrs={'class': 'mod-b-card__car-other'}):
            name_2 = element_2.find_all('span')
            name_2 = name_2[0]
            if name_2 not in Car_Mileage:
                Car_Mileage.append(name_2.text)
                
        #3. Transmission
        for element_3 in soup.find_all(attrs={'class': 'mod-b-card__car-other'}):
            name_3 = element_3.find_all('span')
            name_3 = name_3[1]
            if name_3 not in Car_Transmission:
                Car_Transmission.append(name_3.text)
                
        #4. Location
        for element_4 in soup.find_all(attrs={'class': 'mod-b-card__car-other'}):
            name_4 = element_4.find_all('span')
            name_4 = name_4[2]
            if name_4 not in Car_Location:
                Car_Location.append(name_4.text)

        #5. Car Price
        for element_5 in soup.find_all(attrs={'class': 'mod-card__price__total'}):
            name_5 = element_5.find('strong')
            if name_5 not in Car_Price:
                Car_Price.append(name_5.text)
        #remove new line
        Car_Price = [e.strip().replace('\n', '') for e in Car_Price if e != '']
        # Remove extra spaces
        Car_Price = [' '.join(item.split()) for item in Car_Price]

        #6. Car Instalment Monthly Amount
        for element_6 in soup.find_all(attrs={'class': 'mod-tooltipMonthPay'}):
            name_6 = element_6.find('span')
            if name_6 not in Car_Instalment_Monthly_Amount:
                Car_Instalment_Monthly_Amount.append(name_6.text)
        #remove new line
        Car_Instalment_Monthly_Amount = [e.strip().replace('\n', '') for e in Car_Instalment_Monthly_Amount if e != '']
        # Remove extra spaces
        Car_Instalment_Monthly_Amount = [' '.join(item.split()) for item in Car_Instalment_Monthly_Amount]
        driver.quit()

#dataframe
def load_csv():
    extract_data()
    df = pd.DataFrame({'Names': car_name, 
                    'Car Mileage' : Car_Mileage, 
                    'Transmission' : Car_Transmission,
                    'Car Location' : Car_Location,
                    'Car Price' : Car_Price,
                    'Car Instalment Monthly Amount' : Car_Instalment_Monthly_Amount})

    # df.to_csv('carsome_data.csv', index=False, encoding='utf-8')
    # print(df)
    return df

# # RUN
# if __name__ == "__main__":
#     load_csv()
# #print(df)