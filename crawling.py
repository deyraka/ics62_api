import requests
import json
import mysql.connector
import logging
# from requests.models import cookiejar_from_dict

#initiate variable
session = requests.session()
token = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ7XCJpZFwiOlwiRDVFRjM3RkYtREMwNS00QTYxLUE3MzAtMzZEQkQ1QjlERjg1XCIsXCJ1c2VybmFtZVwiOlwicHJvdl82MlwiLFwiZnVsbG5hbWVcIjpcIkFkbWluIEJQUyBQcm92aW5zaSBLYWxpbWFudGFuIFRlbmdhaFwiLFwiZW1haWxcIjpcInByb3ZfNjJAZ21haWwuY29tXCIsXCJyb2xlSWRcIjpcIjY0RkZCNEM3LTYwRDQtNDQ0Ri1BQjIwLUI2NjRBQjhDRThEOFwiLFwicm9sZU5hbWVcIjpcIkJQUyBQUk9WSU5TSSBBRE1JTlwiLFwicHJvdmluY2VJZFwiOlwiNTEwMjA5NUYtMDIyMi00NThGLUI4RDUtMEI1ODQwRjQ2OUI4XCIsXCJwcm92aW5jZU5hbWVcIjpcIkthbGltYW50YW4gVGVuZ2FoXCIsXCJyZWdlbmN5SWRcIjpudWxsLFwicmVnZW5jeU5hbWVcIjpudWxsLFwid29ya1VuaXRJZFwiOlwiQzM4QzU2NjctM0JCMC00NDNDLUE0MzUtMUVFQ0Q3QzZERkEyXCIsXCJ3b3JrVW5pdE5hbWVcIjpcIkJBREFOIFBVU0FUIFNUQVRJU1RJS1wifSIsImF1ZCI6Im5vbi1jYXdpIiwiZXhwIjoxNjQwNDc2NTM5LCJyb2wiOiJCUFMgUFJPVklOU0kgQURNSU4ifQ.CGFYzqqEv6TYC60GC5gmX1d-myq2knpIRZEPQ5-gsLYVacgxQyBr_faI_nvQ0q0bOzbPUxXOYCbfwy0LAf-8aQ'
cookie = '_ga=GA1.3.2098390205.1575596407; anova2=GA1.3.805240235.1609971573'
regencyId = {"kobar":"9716A5B4-F768-42EB-8EBB-90AAB6B22DDB", "kotim": "A4B7C36F-256E-4853-A6D3-DF970247D172", "palangka": "7D08C1F1-3AD3-4115-BDF3-EED00B633528"}
totalRecord = 0
startOfQuery = 0    #untuk parameter start pada payload yang dikirim bersama method POST ke url_API
lenghtOfQuery = 1000  #untuk parameter lenght pada payload yang dikirim bersama method POST ke url_API
crawledDataLenght = startOfQuery      #untuk mengukur panjang data yang telah berhasil di crawling. digunakan untuk batasan nilai iterasi saat crawling 

url = 'https://api-coolsis.bps.go.id/survey-collection-management/api/assignment/datatable-all-user-survey-periode'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0', 
            'Accept': 'application/json', 
            'Content-Type': 'application/json', 
            'Authorization': token,
            'Cookie': cookie,
            'Connection': 'keep-alive'}

#now we will Create and configure logger 
logging.basicConfig(filename="crawling.log", 
					format='%(asctime)s %(message)s', 
					filemode='w') 
#Let us Create an object 
logger=logging.getLogger() 
#Now we are going to Set the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG)




#fungsi untuk memperbaharui parameter payload
#paramater => start or regencyId
def setPayload(draw = 2, start = 0, kabko = None):
    return {'draw':draw,'columns':[{'data':'id','name':'','searchable':True,'orderable':False,'search':{'value':'','regex':False}},{'data':'code_identity','name':'','searchable':True,'orderable':False,'search':{'value':'','regex':False}},{'data':'data1','name':'','searchable':True,'orderable':True,'search':{'value':'','regex':False}},{'data':'data2','name':'','searchable':True,'orderable':True,'search':{'value':'','regex':False}},{'data':'data3','name':'','searchable':True,'orderable':True,'search':{'value':'','regex':False}},{'data':'data4','name':'','searchable':True,'orderable':True,'search':{'value':'','regex':False}},{'data':'data5','name':'','searchable':True,'orderable':True,'search':{'value':'','regex':False}},{'data':'code_master','name':'','searchable':True,'orderable':False,'search':{'value':'','regex':False}},{'data':'assignment_status_alias','name':'','searchable':True,'orderable':False,'search':{'value':'','regex':False}},{'data':'current_user_fullname','name':'','searchable':True,'orderable':False,'search':{'value':'','regex':False}},{'data':'province_name','name':'','searchable':True,'orderable':False,'search':{'value':'','regex':False}},{'data':'regency_name','name':'','searchable':True,'orderable':False,'search':{'value':'','regex':False}},{'data':'district_name','name':'','searchable':True,'orderable':False,'search':{'value':'','regex':False}},{'data':'village_name','name':'','searchable':True,'orderable':False,'search':{'value':'','regex':False}},{'data':'blok_sensus_fullcode','name':'','searchable':True,'orderable':False,'search':{'value':'','regex':False}}],'order':[{'column':0,'dir':'asc'}],'start':start,'length':lenghtOfQuery,'search':{'value':'','regex':False},'assignmentExtraParam':{'provinceId':None,'regencyId':kabko,'districtId':None,'villageId':None,'blokSensusId':None,'pencacahId':None,'assignmentErrorStatusType':-1,'surveyPeriodeId':'D38BED9C-6B1E-49C3-A22F-08B952F6A84E','surveyId':None,'listUser':[],'roleIndex':None,'data1':None,'data2':None,'data3':None,'data4':None,'data5':None,'assignmentStatusAlias':None}}

#fungsi untuk memperoleh totalRecord
def getTotalRecord(link, header, regencyId):
    #using global variable
    global totalRecord
    #begining of function alghoritm
    payload_for_count = setPayload(2,0,regencyId)
    response = session.post(link, headers=header, json=payload_for_count)
    json_data = json.loads(response.text)
    data_rec = json_data.get('recordsTotal')
    totalRecord = data_rec
    print(totalRecord)
    return totalRecord

#fungsi untuk mulai crawling data
def getData(link, header, lenght, regencyId):
    #using global variable
    global startOfQuery
    global crawledDataLenght
    #begining of function alghoritm
    for key, value in regencyId.items():
        print("Start Crawling RegencyId : " + key)
        startOfQuery = 0 #back to zero per kab/ko
        totalData = getTotalRecord(link, header, value)
        for x in range(startOfQuery, totalData, lenght):
            print("start : " + str(x))
            payload = setPayload(2,x, value)
            response = session.post(link, headers=header, json=payload)
            json_data = json.loads(response.text)
            data = json_data.get('data')
            insertToMySQL(data)

            crawledDataLenght += len(data)
            startOfQuery += crawledDataLenght
            print("Total record right now : " + str(crawledDataLenght))
    else:
        print("Crawling all data is Complete")
   
#fungsi untuk input data ke mysql
def insertToMySQL(data):
    row = 0
    #connect to DB
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="crawl_pplf"
    )
    mycursor = mydb.cursor()
    sql = "REPLACE INTO data (id, kode_identitas, no_urut_kelg, no_urut_ruta, nama_kk, kabko, kec, keldes, kode_bs, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    # val = []
    # for x in data:
    #     # print(x['assignmentStatusAlias'], x['bloksensusFullcode'], x['data4'], x['data5'])
    #     values = [x['id'], x['codeIdentity'], x['data2'], x['data3'], x['data4'], x['regencyName'], x['districtName'], x['villageName'], x['bloksensusFullcode'], x['assignmentStatusAlias']]
    #     val.append(values)
    #     # print(val)

    # mycursor.executemany(sql, val)

    # mydb.commit()

    # print(mycursor.rowcount, "was inserted into database.")
    for x in data:
        try:
            values = [x['id'], x['codeIdentity'], x['data2'], x['data3'], x['data4'], x['regencyName'], x['districtName'], x['villageName'], x['bloksensusFullcode'], x['assignmentStatusAlias']]
            mycursor.execute(sql, values)
            mydb.commit()
            row += mycursor.rowcount
            print(row, " berhasil di insert!")
            logging.info(str(x['id']) + "" + str(x['data3']) + " was inserted.")
        except mysql.connector.Error as error:
            mydb.rollback()
            print("failed to insert {}".format(error))
            logging.error(str(x['id']) + "" + str(x['data3']) + " was failed to insert.")

# getTotalRecord(url, headers)
getData(url, headers, lenghtOfQuery, regencyId)



