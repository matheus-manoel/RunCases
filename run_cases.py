from bs4 import BeautifulSoup
import getpass
import inspect
import os
import requests
import sys

#function tha handles the login
def login(c, username, password):
    login_url = 'https://run.codes/Users/login'
    c.get(login_url)
    payload = {
            'data[User][email]':username,
            'data[User][password]':password
            }
    c.post(login_url, data=payload, headers={'REFERER': 'https://run.codes/'})  

'''

_function: find_cases_number(url, c)
_parameters: url of the exercise, c
_return: list with the end of the urls of each test case

'''
def find_cases_number(url, c):
    urls_end = []                                       #end of urls list
    page = c.get(url)                                   
    soup =BeautifulSoup(page.content)
    for option in soup.find_all('option'): #elements with the tag option have the urls end
        if option['value'].encode('ascii') != '-1': #-1 is the "choose an option" option
            urls_end.append(option['value'].encode("ascii"))    
    return urls_end;                                    #returning urls_end

'''
_function: download_cases(c, exercise_number, current_dir, idx)
_parameters: c, exercise_number is the url_end, current_directory for creating the file, index 
            for the name of the file, essay number represents the essay's code.
_return: void

_does: access the page with the case tests and soupify it; creates 2 files and write on them the
      test cases and expected answers.
'''
def download_cases(c, exercise_number, current_dir, idx, essay_number):
    #page with test cases
    url = 'https://run.codes/CommitsExerciseCases/viewCase/' + str(exercise_number) 
    soup = BeautifulSoup(c.get(url).content)                                        
    input_file = open(current_dir + essay_number + '/inputs/' +str(idx)+'.txt', 'w')
    expected_out_file = open(current_dir + essay_number + 
                                '/expected_outputs/'+str(idx)+'.txt', 'w') 
     #elements with this tag contains 
    pres = soup.find_all('pre')                    
    input_file.write(pres[0].text)                  #write test cases on file1
    expected_out_file.write(pres[1].text)           #write expected outputs on file2
    input_file.close()                      
    expected_out_file.close()

username = raw_input('Email: ')
password = getpass.getpass()
with requests.Session() as c:
    login(c, username, password)
    
    print('\t\tMENU')
    print('1. Baixar casos de todos os trabalhos ativos.')
    print('2. Baixar casos de um trabalho especifico.')
    
    option = int(input('Opcao desejada: '))
    while option < 1 or option > 2:
        option = int(input('Codigo invalido. Tente novamente: '));
    
    if option == 1:
        print('Indisponivel no momento.')
        sys.exit(1)
        #todo: get list of pages
    elif option == 2:
        essay_url = raw_input('URL do trabalho: ');
        essay_number = essay_url.split("view", 1)[1];
    
    urls_end = find_cases_number(essay_url, c)
    current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    if not os.path.exists(current_dir + essay_number):
        os.mkdir(current_dir + essay_number, 0755)
        os.mkdir(current_dir + essay_number + '/inputs', 0755)
        os.mkdir(current_dir+ essay_number + '/expected_outputs', 0755)
    for idx, url in enumerate(urls_end):
        print("Baixando caso %s" % idx)
        download_cases(c, url, current_dir, idx, essay_number)
    print("Todos os arquivos foram baixados.")
    
    # Testing pep8 speaks
