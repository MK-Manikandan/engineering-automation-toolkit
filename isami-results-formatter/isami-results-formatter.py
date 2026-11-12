'''
    To convert the format of ISAMI output file- 'results_total', to element wise format.
    The output file path should be mentioned in the code. 
    Input file is in csv format.
    Output file is in xlsx format.
    Numerical data starts in cell b3
    Paths of the input files should be provided through 'paths.xlsx' file
    where the paths are in cells A1, A2, A3, ...
    The backslashes in paths are to be replaced with forward slashes using cntrl+H
    as python interprets backslashes as escape character.
'''

import xlwings as xw
import sys
import traceback

newpath='Give path here'

try:
    #initializing
    app=xw.App(visible=False)
    wb=xw.Book(r"give excel file path here")
    ws=wb.sheets[0]
    paths=ws.range('a1').expand().value
    if isinstance(paths, str): paths=[paths]
    wb.close()
    print('\n         *****Paths read successfully*****\n')

    #looping through the paths
    for path in paths:
        filename=path.split("/")[-1]
        filename=filename.replace('.csv','')
        print(f'Opening {path}')
        wb=xw.Book(path)
        ws=wb.sheets[0]
        headers=ws.range('d2:i2').value
        data=ws.range('b3').expand('down').expand('right').value
        elem=ws.range('b3').expand('down').value
        elems=list()
        for i in elem:
            if i not in elems: elems.append(i)
        del elem

        #creating new file
        wbnew=xw.Book()
        ws2=wbnew.sheets[0]

        #Entering the load names
        loadname=[i[1] for i in data]
        loadnames=list()
        for i in loadname:
            if i not in loadnames: loadnames.append(i)
        ws2.range('b3').options(transpose=True).value=loadnames

        #adding seriel number
        ws2.range('a3').options(transpose=True).value=list(range(1,len(loadnames)+1))
        del loadname, loadnames

        #Main loop; looping through each elements
        j=3
        for elem in elems:
            eachelem=[i[2:] for i in data if i[0]==elem]
            ws2.range(3,j).value=eachelem
            ws2.range(1,j).value=elem.replace('nid:','')
            ws2.range(2,j).value=headers
            j+=6
        newfilepath=newpath+filename+'_Formatted.xlsx'
        wb.save()
        wb.close()
        wbnew.save(newfilepath)
        wbnew.close()
        print('Done')

except Exception:
    print('Ouch, some error happened')
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print('\n', exc_traceback, '\n', exc_value, '\n', exc_traceback, '\n')
    traceback.print_exc()

finally:
    app.quit()
    print('Run finished')


'''
        Manikandan M
        manikantanm07mk@gmail.com
        14 Jan 2025
'''
