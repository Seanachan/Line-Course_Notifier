import requests
from bs4 import BeautifulSoup

def check_course_availability(course_code):
    url = "https://course.ncku.edu.tw/index.php?c=qry11215&m=en_query"
    
    params = {
        "c": "qry11215",
        "m": "en_query",
        "course_code": course_code  # Example: "HIST001"
    }
    
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the quota section (Update the selector based on actual HTML)
    quota_element = soup.find("td", class_="some_class_name")  # Replace with actual class
    if quota_element:
        available_slots = int(quota_element.text.strip())
        return available_slots
    return None

