
import requests, bs4, smtplib, ssl, datetime
from email.message import EmailMessage
from urllib.parse import urljoin

    
results = requests.get("https://www.thefreshmarket.com/specials/little-big-meal")
results.encoding = "utf-8"
cleanup = bs4.BeautifulSoup(results.text, 'html.parser')
meal_elements = cleanup.select('div[class^="ItemGrid_TwoByTwoMd__"]')
  
# creating list       
global list 
list = [] 

for meal_element in meal_elements:
  title_element = meal_element.select('h3[class^="LBMCard_CardTitle_"]')
  subtitle_element = meal_element.select('p[class^="LBMCard_CardSubtitle__"]')
  available_element = meal_element.select('div[class^="LBMCard_CardTag__"]')
  meal_link_element = next(
    (link for link in meal_element.select('a[href]')
     if link.get_text(" ", strip=True).lower() == "view meal"),
    None
  )
  if meal_link_element is None:
    raise ValueError(f'Could not find "View Meal" link for {title_element[0].get_text(strip=True)}')
  mealLink = urljoin(results.url, meal_link_element["href"])

  list.append(available_element[0].text)
  list.append("Meal: " + title_element[0].text)
  list.append("Description: " + subtitle_element[0].text)
  list.append("Link to meal: " + mealLink)
  list.append("\r\n")
    
port = 465  # For SSL
password = "<password>"
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
  server.login(<Username>, password)
  msg = EmailMessage()
  body = "\r\n".join(list)
  msg.set_content(body)
  msg['Subject'] = 'Upcoming Little Big Meals'
  msg['From'] = "<From Address>"
  msg['Bcc'] = "<To Address>"


  server.send_message(msg)
  server.quit()
