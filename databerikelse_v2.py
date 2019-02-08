import csv
import requests
import ssl
import json

def jsonParser(rest_get_return_list):
    ret_list = []
    for l in rest_get_return_list:
        json_obj   = json.loads(l[1])
        postnummer = json_obj["adresser"][0]["postnummer"]
        poststed   = json_obj["adresser"][0]["poststed"]
        ret_list.append([l[0], postnummer, poststed])

    return ret_list

def restGet(url, parameter_vals, parameter_names):
    
    returner = []
    starter = True
    row_count = 0
    for val_row in parameter_vals:
        row_count += 1
        print(row_count)
        if row_count == 10:
            break
        if starter == True:
            starter = False
            continue
        #print(parameter_names[0], val_row[0], parameter_names[1], val_row[1])
        # https://ws.geonorge.no/adresser/v1/sok?adressenavn=STOVNER%20SENTER&nummer=24&treffPerSide=10&side=0
        url_full = url+"?"+parameter_names[0]+"="+val_row[0]+"&"+parameter_names[1]+"="+val_row[1]
        #print(url_full)
        response = requests.get(url_full, verify=False)
        #print(response)
        #print(type(response.status_code), type(response.text))
        returner.append([response.status_code, response.text])
    return returner

def rowListToDictList(row_list, parameter_names):

    tuple_list = []
    row_count = 0
    for row in row_list:
        row_count += 1
        # Split by first number occurence
        counter = 0
        for char in row:
            #print(char)
            #print(counter)
            if char in ['0','1','2','3','4','5','6','7', '8', '9']:
                #print(row_count)
                break
            counter += 1
        #print(counter)
        print(row_count)
        address = row[0:counter]
        number  = row[counter: len(row)]
        tuple_list.append([address, number])

    #return parameter_dict_list
    return tuple_list


def rowValueExtractorCsv(csv_mtrx, val_col_idx):
    col_val_list = []
    row_count = 0
    for row in csv_mtrx:
        col_val_list.append(row[val_col_idx])
        if row_count == 10:
            break
        row_count += 1
    return col_val_list
#END rowValExtractorCsv()

def fileJoiner(csv_beriket, csv_file, beriket_out):

    in1 = csv_file
    in2 = beriket_out
    out = 

def main2():
    f               = open(csv_file, mode = 'r', encoding='utf-8')
    csv_mtrx        = csv.reader(f, delimiter=';', quotechar='"')
    
    csv_row_list                = rowValueExtractorCsv(csv_mtrx, val_col_idx)
    f.close()
    # print(csv_row_list)
    parameter_vals              = rowListToDictList(csv_row_list, parameter_names) #list of 'tuples'
    # print(parameter_dict_list)
    rest_get_return_list        = restGet(url, parameter_vals, parameter_names)
    
    print(rest_get_return_list)
    parsed_return_list          = jsonParser(rest_get_return_list)
    print(parsed_return_list)
    beriket = []
    row_count = 0
    for row in parameter_vals[1: len(parsed_return_list)]:
        berikelses_str = row[0]+row[1]+"; "+parsed_return_list[row_count][1]+"; "+parsed_return_list[row_count][2]+"; "+str(parsed_return_list[row_count][0])+"\n"
        beriket.append(berikelses_str)
        row_count += 1

    f = open(beriket_out, mode='w+', encoding='utf-8')
    f.write("adresse; postnummer; poststed; feilkode_web\n")
    for b in beriket:
        f.write(b)
    f.close()

    fileJoiner(csv_beriket, csv_file, beriket_out)

################ Konfigurasjon ##############################
# EXCEL KONFIG ##############################################
# Excel Filename
excel_file      = "C:\\Users\\Work\\Desktop\\Miljøhack\\Data fra REN og EGE - Mod\\innsamlingsdata_fjernet_kolonner.xlsx"
csv_file        = "C:\\Users\\Work\\Desktop\\Miljøhack\\Data fra REN og EGE - Mod\\innsamlingsdata_fjernet_kolonner.csv"
rest_out        = "C:\\Users\\Work\\Desktop\\Miljøhack\\Data fra REN og EGE - Mod\\rest_out.txt"
beriket_out     = "C:\\Users\\Work\\Desktop\\Miljøhack\\Data fra REN og EGE - Mod\\beriket_out.csv"

csv_beriket     = "C:\\Users\\Work\\Desktop\\Miljøhack\\Data fra REN og EGE - Mod\\beriket_final.csv"
# Excel extract
val_col_idx  = 3
ctrl_col_idx = 0
# Split
split_by    = " "

# REST KONFIG ###############################################
url             = "https://ws.geonorge.no/adresser/v1/sok"
parameter_names = ["adressenavn","nummer"]
#############################################################

main2()
