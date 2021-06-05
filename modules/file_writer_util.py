# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 10:43:40 2021

@author: Eric.Gomez-V@unilever.com
"""
from pandas import ExcelWriter
from progress.bar import ShadyBar


def dict_to_excel(dict_sheetNames_dfs:dict, fileName:str):
    """
    escribe dataFrames en un archvivo de excel
    """
    print('Writing file: ',fileName)
    sheetNameList = list(dict_sheetNames_dfs.keys())
    dataFrameList = list(dict_sheetNames_dfs.values())
    def column_string(n:int):
        """
        regresa el index de columna de excel con base en el numero n de columnas
        """
        string = ""
        while n > 0:
            n, remainder = divmod(n - 1, 26)
            string = chr(65 + remainder) + string
        return string

    writer = ExcelWriter(# pylint: disable=abstract-class-instantiated
        path=fileName, engine='xlsxwriter')  
    workbook = writer.book # pylint: disable=no-member
    header_format = workbook.add_format({'bold': True, 'align': 'center',
                                         'fg_color': '#80bfff', 'border': 2,
                                          'font_name': 'Times New Roman', 'font_size': 9})
    body_format = workbook.add_format(
        {'border': 1, 'align': 'left', 'font_name': 'Times New Roman', 'font_size': 9})
    bar = ShadyBar("Loading...", max=len(dataFrameList), suffix='%(percent)d%%')
    indexSheet = 0
    for dataFrame in dataFrameList:
        letraInicial = "A"
        letraFinal = column_string(len(dataFrame.columns))
        letrasColXlsx = [column_string(i)
                         for i in range(1, len(dataFrame.columns)+1)]
        lenColNames = [len(col) for col in dataFrame.columns]
        lenFirstColReg = [len(max(list(map(lambda x: str(x),dataFrame[col].tolist()))))
                          for col in dataFrame.columns]
        dataFrame.to_excel(
            writer, sheet_name=sheetNameList[indexSheet], index=False)
        worksheet = writer.sheets[sheetNameList[indexSheet]]
        if len(letrasColXlsx) == len(lenColNames):
            for i in range(len(letrasColXlsx)):
                if lenColNames[i] > lenFirstColReg[i]:
                    worksheet.set_column(
                        letrasColXlsx[i]+':'+letrasColXlsx[i], lenColNames[i], body_format)
                else:
                    worksheet.set_column(
                        letrasColXlsx[i]+':'+letrasColXlsx[i], lenFirstColReg[i], body_format)
        for col_num, value in enumerate(dataFrame.columns.values):
            worksheet.write(0, col_num, value, header_format)
        worksheet.autofilter(letraInicial+'1:'+letraFinal+'1')
        if "complete" in sheetNameList[indexSheet]:
            worksheet.hide()
        indexSheet += 1
        bar.next()
    print("\n")
    writer.save()
