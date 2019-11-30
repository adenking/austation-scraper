

from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import csv
import tqdm

def Download_Data(url):
    request = requests.get("https://stats.austation.net/deaths/" + str(url))
    soup = BeautifulSoup(request.content,'html.parser')
    try:
        page_status = soup.find('span', {'class': 'badge badge-dam badge-brute'}, text='BRU').get_text()
    except:
        page_status = None
    if page_status == 'BRU':
        pass
    else:
        death_id = url

        username = soup.find('h2')
        username = username.get_text()[10:].strip().split('/')
        username, player_namer = username[0], username[1]

        #player_name = soup.find('small', {'class': 'text-right align-middle'}, text='Station Name')
        #player_name = player_name.findNext('td')
        #player_name = player_name.get_text().strip()

                
        #with open('deaths.csv', 'a') as f:
        #    writer = csv.writer(f, delimiter=',')
        #    writer.writerow([death_number, username, player_name, rank, cause_of_death, brute_damage, brain_damage, fire_damage, oxy_damage, tox_damage, clone_damage, stamina_damage, murder_suspect])

if __name__ == '__main__':
    Download_Data('26040')
    #pool = Pool(processes=10)
    #for _ in tqdm.tqdm(pool.imap_unordered(Download_Data, range(25915)), total=25915):
    #    pass
