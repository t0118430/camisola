import requests
from bs4 import BeautifulSoup
import os
from twilio.rest import Client

url = os.getenv('URL')
to = os.getenv('TO')
from_ = os.getenv('FROM')
account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
send_notification = os.getenv('SEND_NOTIFICATION')
class_name = 'no-stock-label'
disable_click = 'disable-click'

def check_class_div_present(url, class_name, disable_click):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all divs with the specified class
            p_with_class = soup.find_all('p', class_=class_name)

            li_with_class = soup.find_all('li', {'data-size': 5, 'class': disable_click})

            # Check if any divs with the class were found
            if p_with_class and li_with_class:
                print(f"Indisponível.")
                return False
            else:
                print(f"Disponível.")
                return True
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"An error occurred while trying to retrieve the webpage: {e}")
        return False

if check_class_div_present(url, class_name, disable_click) and send_notification.upper() == 'S':
        client = Client(account_sid, auth_token)
        message = client.messages.create(
        to=to,
        from_=from_,
        body=f'Camisola Disponivel schnell!'
        )