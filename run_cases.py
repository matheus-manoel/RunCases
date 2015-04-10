
import requests
import getpass
from bs4 import BeautifulSoup
import os
import inspect

#function tha handles the login
def login(c, username, password):
    login_url = 'https://run.codes/Users/login'
    c.get(login_url)
    payload = {
            'data[User][email]':username,
            'data[User][password]':password
            }
    c.post(login_url, data=payload, headers={'REFERER': 'https://run.codes/'})        
                
def find_cases_number(url, c):
    urls_end = []
    page = c.get(url)
    soup = BeautifulSoup(page.content)
    #print soup.prettify()
    for option in soup.find_all('option'):
        if option['value'].encode('ascii') != '-1':
            urls_end.append(option['value'].encode("ascii"))
            #print 'value: {}, text: {}'.format(option['value'], option.text)
    return urls_end;

def download_cases(c, exercise_number, current_dir, idx):
    url = 'https://run.codes/CommitsExerciseCases/viewCase/' + str(exercise_number)
    soup = BeautifulSoup(c.get(url).content)
    input_file = open(current_dir+'/141/inputs/'+str(idx)+'.txt', 'w')
    expected_out_file = open(current_dir+'/141/expected_outputs/'+str(idx)+'.txt', 'w')
    pres = soup.find_all('pre')
    input_file.write(pres[0].text)
    expected_out_file.write(pres[1].text)
    input_file.close()
    expected_out_file.close()

username = raw_input('Email\n')
password = getpass.getpass()
with requests.Session() as c:
    login(c, username, password)
    #todo: get urls of 
    urls_end = find_cases_number('https://run.codes/exercises/view/141', c)
#    print urls_end
    current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    if not os.path.exists(current_dir+'/141'):
        os.mkdir(current_dir+'/141', 0755)
        os.mkdir(current_dir+'/141/inputs', 0755)
        os.mkdir(current_dir+'/141/expected_outputs', 0755)
#    download_cases(c, urls_end[0], current_dir, 0)
    for idx, url in enumerate(urls_end):
        download_cases(c, url, current_dir, idx)
    #for url in urls_end:
     #   download_cases(c, url) 
