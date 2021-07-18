import pandas as pd
import requests
import asyncio
from datetime import datetime as dt
import numpy as np
import traceback
import time

appl_doc = pd.read_excel('application_documents.xlsx')
appl_doc_false = pd.read_excel('application_documents_FALSE.xlsx')

appl_doc_files = appl_doc.copy()
appl_doc_files['path'] = ''

appl_doc_false_files = appl_doc_false.copy()
appl_doc_false_files['path'] = ''

agent_str = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'


def get_links(links):
    """
    Extract links from string
    :param links: list with links
    :return: list with encapsulated links
    """
    return_list = []
    for link in links:
        if 'http' in link:
            current_list = eval(link)
            current_list = [my_str.replace('"', '') for my_str in current_list]
            return_list.append(current_list)
        else:
            return_list.append(None)
    return return_list


def request_link(links):
    saved_names = []
    if 'list' in str(type(links)):
        for link in links:
            try:
                r = requests.get(link, headers={'user-agent': agent_str})
                current_name = f'data/doc_{dt.now().strftime("%H%M%S")}_{str(np.random.randint(1000))}'
                with open(current_name, 'wb') as f:
                    f.write(r.content)
                saved_names.append(current_name)
            except Exception as e:
                my_error = f'\n\nException on {link}:\n{str(e)}\nTraceback:\n{traceback.format_exc()}'
                saved_names.append(my_error)
                print(my_error)
                print(f'Sleep for 3 sec')
                time.sleep(3)
        print(f'Sleep for 0.5 sec')
        time.sleep(0.5)
    else:
        saved_names = None
    return saved_names


async def appl_doc_fun():
    for i in range(0, len(appl_doc)-4, 3):
        print(f'\n\nString: {i} from {len(appl_doc)}')
        links = get_links([appl_doc['files'][i], appl_doc['files'][i+1], appl_doc['files'][i+2]])
        loop = asyncio.get_event_loop()
        future1 = loop.run_in_executor(None, request_link, links[0])
        future2 = loop.run_in_executor(None, request_link, links[1])
        future3 = loop.run_in_executor(None, request_link, links[2])
        response1 = await future1
        response2 = await future2
        response3 = await future3
        appl_doc_files['path'].iloc[i] = response1
        appl_doc_files['path'].iloc[i+1] = response2
        appl_doc_files['path'].iloc[i+2] = response3
        print('Success!')

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(appl_doc_fun())
except Exception as e:
    print(f'excpetion: {str(e)}, traceback: {traceback.format_exc()}')

appl_doc_files.to_excel('appl_doc_files.xlsx')
print('\n\n\nAPPL DOC FINISHED!!!\n\n\n')

async def appl_doc_false_fun():
    for i in range(0, len(appl_doc_false)-4, 3):
        print(f'\n\nString: {i} from {len(appl_doc_false)}')
        links = get_links([appl_doc_false['files'][i], appl_doc_false['files'][i+1], appl_doc_false['files'][i+2]])
        loop = asyncio.get_event_loop()
        future1 = loop.run_in_executor(None, request_link, links[0])
        future2 = loop.run_in_executor(None, request_link, links[1])
        future3 = loop.run_in_executor(None, request_link, links[2])
        response1 = await future1
        response2 = await future2
        response3 = await future3
        appl_doc_false_files['path'].iloc[i] = response1
        appl_doc_false_files['path'].iloc[i+1] = response2
        appl_doc_false_files['path'].iloc[i+2] = response3
        print('Success!')

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(appl_doc_false_fun())
except Exception as e:
    print(f'excpetion: {str(e)}, traceback: {traceback.format_exc()}')


appl_doc_false_files.to_excel('appl_doc_false_files.xlsx')
