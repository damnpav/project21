import pandas as pd
import requests
import traceback
import re
from datetime import datetime as dt
import time

#zakupki_links = [link.replace('\n', '') for link in open('zakupki_links.txt').readlines() if link != '\n']
zakupki_links = pd.read_excel('selected tender links.xlsx')
tender_list = zakupki_links['tenderlink'].tolist()
link_list = list(set(tender_list))


def get_regnumber(link):
    return re.findall('=\d.*', link)[0][1:]

reg_search_str = open('reg_search_str.txt').read()
contract_card = open('contract_card.txt').read()
agent_str = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'

def link_parser(link):
    custom_str = reg_search_str.replace('your_str', get_regnumber(link))
    r = requests.get(custom_str, headers={'user-agent': agent_str})
    if r.status_code != 200:
        return f'Error with search of contract! {r.status_code}'
    reestr_list = re.findall('reestrNumber=\d+"', r.text)
    if len(reestr_list) == 0:
        return 'There are no contracts'
    if len(list(set(reestr_list))) > 1:
        print('len(contracts) > 1 !!!')
    reestr_number = re.findall('\d+', reestr_list[0])[0]
    card_address = contract_card.replace('your_str', reestr_number)
    r = requests.get(card_address, headers={'user-agent': agent_str})
    if r.status_code != 200:
        return 'Error with search of contract card!'
    links_list = re.findall('http.*filestore.*"', r.text)

    if len(links_list) == 0:
        return 'Documents are not found'
    else:
        return links_list


k = 0
links_df = pd.DataFrame(columns=['link', 'files'])
for link in link_list:
    k += 1
    print(f'Count is: {str(k)}/{len(link_list)}')
    print(f'\n\n{dt.now().strftime("%H:%M:%S")}: Link is {link}')
    try:
        link_result = link_parser(link)
        print(f'\n\n{dt.now().strftime("%H:%M:%S")}: Result is {link_result}')
        links_df = links_df.append({'link': link, 'files': link_result}, ignore_index=True)
    except Exception as e:
        print(f'\n\n{dt.now().strftime("%H:%M:%S")}: Exception: {str(e)} \n\nTraceback: {traceback.format_exc()}')
        links_df = links_df.append({'link': link, 'files': str(e)})

    print('Sleep 0.25...')
    time.sleep(0.25)

links_df.to_excel('application_documents.xlsx')







