from os import listdir
from datetime import datetime
from pandas import  read_excel, DataFrame, concat

def filter_listdir(folder:str, extension: str) -> list:
    ''' Returns a filtered files of a given folder'''
    files = list(filter(
        lambda item:
            str(item).split('.')[-1] == extension,
        listdir(folder)
    ))
    return [folder+file for file in files]

def concat_logs(list_files: list) -> DataFrame:
    ''' Function that returns concat of logs in a single dataframe''' 
    df = DataFrame()
    for file in list_files:
        temp_df = read_excel(file)
        df = concat([df,temp_df])
    return df

def main():
    pHead = '''
 _____                                              _     _____ _____      
/  ___|                                            | |   |  _  |  __ \\     
\\ `--. _   _ _ __ ___  _ __ ___   __ _ _ __ _   _  | |   | | | | |  \\/___  
 `--. \\ | | | '_ ` _ \\| '_ ` _ \\ / _` | '__| | | | | |   | | | | | __/ __| 
/\\__/ / |_| | | | | | | | | | | | (_| | |  | |_| | | |___\\ \\_/ / |_\\ \\__ \\ 
\\____/ \\__,_|_| |_| |_|_| |_| |_|\\__,_|_|   \\__, | \\_____/\\___/ \\____/___/ 
                                             __/ |                         
                                            |___/   
--------------------------------------------------------------------------------    
    '''
    paths = {'logs':'logs/'}
    print(pHead)
    files = filter_listdir(paths['logs'], 'xlsx')


main()