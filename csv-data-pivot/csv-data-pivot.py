'''
This program converts resultstotal.csv format to element wise format.
Input format should be:
elem id	    lc name	    Sx_elem_z1	   Sy_elem_z1	 Sxy_elem_z1	Sx_elem_z2
13581330	2DP_1200mb	29.00592422	   51.45750046	 -2.733603001	31.96347618
13581330	ACF_U__ACF	-30.04614258   2.728279352	 26.09137917	-23.83198547
13581330	ACF_U__ACF	-30.27905846   2.714482307	 26.32208633	-24.01170921
13581330	ACF_U__ACF	14.07229137	   -8.47319603	-18.59562111	11.81798363
13581330	ACF_U__ACF	14.05535316	   -8.474822998	-18.58137703	11.80519295

update column count, element count and lc count
update the if loops with the elements that need not to be considered.
update the input file path
'''
import csv

path = "give the csv file path here"

#opening input file
with open(path, 'r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    inlist = list(reader)
    #first element is the list reserved for the element names in the top row
    #first column is for load case names
    outlist = [[None],[None]]
    elements = [] 
    col_count = 13 #number of columns
    elem_count = 128 #number of elements
    lc_count = 2162 #number of load cases
    [outlist.append(list()) for k in range(lc_count)] #creating nested lists, same number as lc

    #looping through load cases
    for i in range(lc_count):
        #avoiding unwanted load cases
        if i == (lc_count - 1) or i == (lc_count - 2):
            continue
        outlist[i+2].append(inlist[i+1][1])
        #looping through elements
        for j in range(elem_count):
            outlist[i+2] += inlist[i + 1 + (j * lc_count)][2:]
            elements.append(inlist[i + 1 + (j * lc_count)][0])

    #filtering unique elements
    unique_elements = []
    [unique_elements.append(x) for x in elements if x not in unique_elements]

    #inserting element names with required spaces
    for l in range(elem_count * col_count):
        if l % col_count == 0:
            outlist[0].append(unique_elements[l // col_count])
        else:
            outlist[0].append(None)

    #inserting headers
    headers=inlist[0]
    headers.pop(0) #removing first two empty cells
    headers.pop(0)
    for m in range(elem_count):
        outlist[1] += headers

    #opening output file
    with open('output.csv', 'w', newline='', encoding='utf-8') as outfile:
        writer=csv.writer(outfile)
        writer.writerows(outlist)

print('Program finished. Output is saved to output.csv')

'''
    Manikandan M
    manikantanm07mk@gmail.com
    https://github.com/MK-Manikandan
    https://www.linkedin.com/in/manikandan--m
    23rd July 2025
'''
