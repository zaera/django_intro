import requests
from bs4 import BeautifulSoup
from grabber import CSVGrabber, JSONGrabber, Sqlite3Grabber
import html2text

ROOT = 'https://www.work.ua'
url = ROOT + '/jobs/?ss=1'

page = 0
check_list = []

grabbers_list = [
    CSVGrabber(),
    JSONGrabber(),
    Sqlite3Grabber(),
]

while True:
    page += 1
    print(f'Page number: {page}')  # noqa

    # if page == 96:
    #     break

    params = {
        'page': page,
    }
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    job_container = soup.find("div", {"id": "pjax-job-list"})
    jobs = job_container.find_all('div', {'class': 'card card-hover card-visited wordwrap job-link js-hot-block'})
    if jobs is None:
        break
    for job in jobs:
        href = job.find('a')['href']
        title = job.find('a').text
        id_ = ''.join(char for char in href if char.isdigit())
        detail = ROOT + '/jobs/' + id_ + '/'
        response_ = requests.get(detail)
        soup_ = BeautifulSoup(response_.text, 'html.parser')
        description = str(
            soup_.find("div", {"class": "card wordwrap"}).find("div", {"id": "job-description"}).text.replace("\n", ""))
        city = str(soup_.find("p", {"class": "text-indent add-top-sm"}).get_text().strip())

        # Salary may be in different sub containers or even Null

        salary = soup_.find("p", {"class": "text-indent text-muted add-top-sm"}).find("b", {"class": "text-black"})
        if salary is None:
            salary = soup_.find("p", {"class": "text-indent text-muted add-top-sm"}).find("span",
                                                                                          {"class": "text-muted"})
            if salary is not None:
                salary = html2text.html2text(salary.text)
                salary = salary.replace("\n", "")
            else:
                salary = ''
        else:
            salary = html2text.html2text(salary.text).replace("\n", "")
            salary = salary.replace("\n", "")

        # Check id if already in list

        if id_ not in check_list:
            print(f'{id_} will be added') # noqa
            data = {
                'id': id_,
                'href': href,
                'title': title,
                'description': description,
                'city': city,
                'salary': salary,
            }

            # Add if not

            check_list.append(id_)
            for grabber in grabbers_list:
                grabber.write(data)

for grabber in grabbers_list:
    grabber.destruct()
