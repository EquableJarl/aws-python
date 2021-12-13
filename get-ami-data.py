#!/usr/bin/env python3
import xlsxwriter
import boto3
import json
import jq

ec2_1 = boto3.client('ec2', region_name='eu-west-1')
ec2_2 = boto3.client('ec2', region_name='eu-west-2')

def fixAwsResponses(data):
    fixingResponse = json.dumps(data, indent=2, sort_keys=True, default=str)
    fixedResponse = json.loads(fixingResponse)
    return fixedResponse

def printDump(worksheet, data, start):
    for count, _ in enumerate(data):
        worksheet.write_column(start, count, data[count])

def getDataDump(data, client):
    amis = jq.all('.Reservations[].Instances[].ImageId'  , data)
    dimages_response = fixAwsResponses(client.describe_images(ImageIds=amis))
    imageIds = jq.all('.Images[].ImageId', dimages_response)
    platfoms = jq.all('.Images[].PlatformDetails', dimages_response)
    names = jq.all('.Images[].Name', dimages_response)
    dataDump = [imageIds, platfoms, names]
    region = []
    for _ in dataDump[0]:
        region.append(client.meta.region_name)
    dataDump.append(region)
    return dataDump

data1 = fixAwsResponses(ec2_1.describe_instances())
dataDump1 = getDataDump(data1,ec2_1)
data2 = fixAwsResponses(ec2_2.describe_instances())
dataDump2 = getDataDump(data2, ec2_2)

############ creating excel spreadsheet #######################

workbook = xlsxwriter.Workbook('amiData.xlsx')
worksheet = workbook.add_worksheet()
cell_format = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color' : 'gray'})
headers = ['ami-id', 'platform', 'ami-name', 'region']

for count, value in enumerate(headers):
    worksheet.write(0, count, value, cell_format)

# TODO write a function to handle this mess at the bottom here...

count = 1
printDump(worksheet, dataDump1, count)
count = count + len(dataDump1[0])
printDump(worksheet, dataDump2, count)

workbook.close()
