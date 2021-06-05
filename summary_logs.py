from os import listdir, system
from os.path import abspath
from datetime import datetime
from pandas import  read_excel, DataFrame, concat
from modules import file_writer_util as FRU

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
        phone = (file.split('/')[-1]).split('.')[0]
        temp_df = read_excel(file)
        temp_df['phone'] = [phone] * temp_df.shape[0]
        df = concat([df,temp_df])
    return df


def get_counts(df: DataFrame) -> dict:
    ''' Function that returns the f'''
    sheets_summary = {
        'concat_logs':df,
        'group_by_type':df.groupby(['type']).size().to_frame().rename(columns={0:'count'}).reset_index(),
        'group_by_phone_type':df.groupby(['phone','type']).size().to_frame().rename(columns={0:'count'}).reset_index(),
        'group_by_phone_lang':df.groupby(['phone','lang']).size().to_frame().rename(columns={0:'count'}).reset_index(),
        'group_by_phone':df.groupby(['phone']).size().to_frame().rename(columns={0:'count'}).reset_index(),
        'group_by_lang':df.groupby(['lang']).size().to_frame().rename(columns={0:'count'}).reset_index(),
    }

    return sheets_summary


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
    '''
    div = '-------------------------------------------------------------------------------- '
    paths = {
        'logs':'logs/',
        'outs':'outs/'
    }
    DATE_NOW = datetime.now().strftime('%d-%m-%YT%H-%M-%S')
    print(pHead)
    print(div)
    files = filter_listdir(paths['logs'], 'xlsx')
    general_df = concat_logs(files)    
    summarys = get_counts(general_df)
    for summary in summarys.keys():
        print(div)
        print('TABLE: ', summary)
        print(summarys[summary],'\n')
    summary_fname = paths['outs']+DATE_NOW+'.xlsx'
    FRU.dict_to_excel(summarys, summary_fname)
    system('del '+abspath(paths['logs'])+'\\*.xlsx')
    system(abspath(summary_fname))

main()