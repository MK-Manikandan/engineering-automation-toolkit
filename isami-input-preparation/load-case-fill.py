'''
    This program copies LC and ULC data from the path given below and pastes it in the paths
    given in the excel file. Columns should be same, if any additional columns are present in between, 
    it should be deleted. It removes data, copies, and pastes only upto column Z and unlimited row, given
    the loadcase labels (first column) is continuous. The source file's paths are to be pasted below as
    r string. The path.xlsx file's path should be updated if directory is changed.
    LCSets sheet is updated according to the load case number in the ulc clc sheets-
    given, the load case number is in column c in ulc and in column b in clc
'''

import xlwings as xw
import sys
import traceback

#required paths; should be give as r string if  backslashes are present
std=r"C:\Users\path\00_STD_ULC_CLC_List.xlsx"
stdlmass=r"C:\Users\path\00_STD_L-Mass_ULC_CLC_List.xlsx"
ps=r"C:\Users\path\00_PS_ULC_CLC_List.xlsx"
pslmass=r"C:\Users\path\00_PS_L-Mass_ULC_CLC_List.xlsx"

kinds=[[std,'std'],[stdlmass,'stdlmass'],[ps,'ps'],[pslmass,'pslmass']]

try:
    #initialising
    app=xw.App(visible=False)
    wb=xw.Book(r"C:\Users\path\Isami_Input_file_format\ULC_CLC_copy_paste\paths.xlsx")
    ws=wb.sheets[0]
    paths=list(ws.range('a1').expand().value)
    wb.close()
    print('\n         *****Paths read successfully*****\n')

    for kind in kinds:
        #for efficiency, approaching the types of files one by one, and then deleting the data after each loop
        wb=xw.Book(kind[0])
        ulc_sheet=wb.sheets('ULC List')
        clc_sheet=wb.sheets('CLC List')
        for path in paths:
            if path[1] != kind[1]: continue
            wb1=xw.Book(path[0])
            ulc_sheet1=wb1.sheets('ULC List')
            clc_sheet1=wb1.sheets('CLC List')
            ulc_sheet1.range('a2:z2').expand('down').clear_contents()
            clc_sheet1.range('a2:z2').expand('down').clear_contents()
            ulc_sheet1.range('a2').value=ulc_sheet.range('a2:z2').expand('down').value
            clc_sheet1.range('a2').value=clc_sheet.range('a2:z2').expand('down').value

            #LCSet
            lc_set_sheet=wb1.sheets('LCSet')
            lc_set_sheet.range('a2:d4').clear_contents()
            lc_set_sheet.range('a2').value='LC_Set_01'
            lc_set_sheet.range('b2').value=str(int(ulc_sheet1.range('c2').value)) + '-' + str(int(ulc_sheet1.range('c2').end('down').value))
            lc_set_sheet.range('c2').value=str(int(clc_sheet1.range('b2').value)) + '-' + str(int(clc_sheet1.range('b2').end('down').value))

            wb1.save()
            wb1.close()
            print(f'Type: {kind[1]} in path ->\n{path[0]}\n finished successfully\n')

        wb.close()
        print(f'\n{kind[1]} type files finished successfully\n\n')
    print('No error happened')

except Exception:
    print('Ouch, some error happened')
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print('\n',exc_traceback,'\n',exc_value,'\n',exc_traceback,'\n')
    traceback.print_exc()

finally:
    app.quit()
    print('Run finished')


'''
        Manikandan M
        manikantanm07mk@gmail.com
        20 Jan 2025
'''
