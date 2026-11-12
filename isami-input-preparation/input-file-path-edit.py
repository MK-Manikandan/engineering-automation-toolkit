'''
    This program changes the BDF_Path in isami input files for extraction, to the given path in the code
    and clears the OP2_FileModel_Path cell, given, BDF path is in cell B4 of sheet 'Analyses'
    The path.xlsx file's path should be updated if directory is changed.
'''
import sys
import xlwings as xw
import traceback

std="path for dat file"
ps="path for dat file"

try:
    app=xw.App(visible=False)
    wb=xw.Book(r"excel file path")
    ws=wb.sheets[0]
    paths=list(ws.range('a1:b1').expand('down').value)
    for path in paths:
        wb1=xw.Book(path[0])
        ws1=wb1.sheets('Analyses')
        ws1.range('b6').clear_contents()
        if path[1]=='std':
            ws1.range('b4').value=std
        else:
            ws1.range('b4').value=ps
        wb1.save()
        wb1.close()
        print(f'{path[1]}  -  {path[0]}\nEdited and closed\n')
    print('No error happened')

except Exception:
    print('Ouch, some error happened')
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print('\n',exc_traceback,'\n',exc_value,'\n',exc_traceback,'\n')
    traceback.print_exc()

finally:
    wb.close()
    app.quit()
    print('Run finished')

'''
        Manikandan M
        manikantanm07mk@gmail.com
        20 Jan 2025
'''
