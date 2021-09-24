
import requests, bs4, smtplib, ssl, datetime
from email.message import EmailMessage

    
results = requests.get("https://www.thefreshmarket.com/specials/little-big-meal")
cleanup = bs4.BeautifulSoup(results.text, 'html.parser')
meal_elements = cleanup.find_all("div", class_="lbm-card")
  
# creating list       
global list 
list = [] 

for meal_element in meal_elements:
  title_element = meal_element.find("h3", class_="lbm-card__title")
  subtitle_element = meal_element.find("p", class_="lbm-card__subtitle")
  available_element = meal_element.find(class_="lbm-card__tag")
  mealLink = "https://www.thefreshmarket.com"+meal_element.contents[0].contents[0].attrs['href']
  list.append(available_element.text)
  list.append("Meal: " + title_element.text)
  list.append("Description: " + subtitle_element.text)
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
  #msg['Bcc'] = "<To Address>"


  server.send_message(msg)
  server.quit()

