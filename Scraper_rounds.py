from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import csv
import tqdm

def Download_Data(url):
    request = requests.get("https://stats.austation.net/rounds/" + str(url))
    soup = BeautifulSoup(request.content,'html.parser')
    try:
        page_status = soup.find('small', {'class': 'text-muted'}).get_text()
    except:
        page_status = None
    if page_status == 'error code':
        pass
    else:
        round_id = url

        station_name = soup.find('th', {'class': 'text-right align-middle'}, text='Station Name')
        station_name = station_name.findNext('td')
        station_name = station_name.get_text().strip()

        escape_shuttle_name = soup.find('th', {'class': 'align-middle text-right'}, text='Escape Shuttle')
        escape_shuttle_name = escape_shuttle_name.findNext('td')
        escape_shuttle_name = escape_shuttle_name.get_text().strip()


        round_duration = soup.find('th', {'class': 'align-middle text-right'}, text='Round Duration')
        round_duration = round_duration.findNext('td')
        round_duration = round_duration.get_text().strip()

        total_deaths = soup.find('th', {'class': 'align-middle text-right'}, text='Deaths')
        total_deaths = total_deaths.findNext('a')
        total_deaths = total_deaths.get_text().strip()
        
        
        complete_status = soup.find('div', {'class': 'badge badge-proper d-block'})
        if complete_status == None:
            complete_status = soup.find('div', {'class': 'badge badge-vote d-block'})
        if complete_status == None:
            complete_status = soup.find('div', {'class': 'badge badge-inverse d-block'})
        if complete_status == None:
            complete_status = soup.find('div', {'class': 'badge badge-reboot d-block'})
        if complete_status == None:
            complete_status = soup.find('div', {'class': 'badge badge-danger d-block'})
        if complete_status == None:
            complete_status = soup.find('div', {'class': 'badge badge-success d-block'})
        if complete_status == None:
            complete_status = soup.find('div', {'class': 'badge badge-warning d-block'})
        complete_status = complete_status.get_text().strip()

        round_type = soup.find('div', {'class': 'col-md-8 col-sm-12 h3 text-center'})
        round_type = round_type.findNext('i')
        round_type = round_type.next_sibling.strip()

        with open('rounds.csv', 'a') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow([round_id, station_name, escape_shuttle_name, round_duration, total_deaths, complete_status, round_type])

if __name__ == '__main__':
    pool = Pool(processes=20)
    for _ in tqdm.tqdm(pool.imap_unordered(Download_Data, range(2584)), total=2584):
        pass
