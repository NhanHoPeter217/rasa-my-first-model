fileCSVURL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSMs5Q2Yzd7J2ViBl0sXm7S75f-2_mXVxkABqAKAZbtENTBDSr1ANP8LYMVEoVUKPpqxxFe40U2wkTb/pub?gid=1295845480&single=true&output=csv'
mapCSVURL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSAWBkVy4eZ0k04ZKEwppDMvCHNlDIxoZXn1H8puT4xqrw-ui4y-rnFRgBaImR7bBg6XGaVul1X279U/pub?gid=1274123795&single=true&output=csv'
outputName = 'data/nlu_from_forms.yml'

import os
import csv
import re
import requests
import io


dataCSV = None
headerMap = None
dataDict = {}
currentPWD = os.path.join(os.getcwd(), '.~scripts')

def fetchDataCSVFromURL(url):
  
  response = requests.get(url)
  data = response.content.decode('utf-8')
  dataFile = io.StringIO(data)
  reader = csv.reader(dataFile)
  return [row for row in reader]


def searchIntent(intent):
  for row in headerMap:
    if row[0] == intent:
      return row[1]
  return None

def addData(intent, data):
  if intent in dataDict:
    dataDict[intent].append(data)
  else:
    print('Intent not found:', intent)
    
def cleanDataDict():
  removeCondition = re.compile(r'^.{0,1}$')
  
  for intent in dataDict:
    dataDict[intent] = list(set(dataDict[intent]))
    dataDict[intent] = [example for example in dataDict[intent] if example != '' and not removeCondition.match(example)]
    dataDict[intent].sort()

def convertToRasaYAML():
  with open(outputName, 'w') as file:
    
    file.write(f'version: "3.1"\n\n')
    file.write(f'nlu:\n')
    
    for intent in dataDict:
      file.write(f'  - intent: {intent}\n    examples: |\n')
      for example in dataDict[intent]:
        file.write(f'      - {example}\n')
      
      file.write('\n')


if __name__ == '__main__':
  print('Fetching data...')
  dataCSV = fetchDataCSVFromURL(fileCSVURL)
  print('Fetching intent mapping...')
  headerMap = fetchDataCSVFromURL(mapCSVURL)
  
  if (dataCSV is None or headerMap is None):
    print('Error fetching data')
    exit(1)
  
  headerRegexMatch = re.compile(r'\d{1,2}-(.+(?:\n.+)?(?:\n.+)?(?:\n.+)?)')
  headerRow = dataCSV[0]

  # Create dataDict
  for formQuestion in headerRow:
    if headerRegexMatch.match(formQuestion):
      intentVietnamese = headerRegexMatch.match(formQuestion).group(1)
      intentEnglish = searchIntent(intentVietnamese)
      
      if intentEnglish:
        dataDict[intentEnglish] = []
      
      if not intentEnglish:
        print('\n[Regex]Matched:', formQuestion)
        print('\t\t[Intent] Not found:', intentVietnamese)
    
    else:
      print('[Regex]Invalid header:', formQuestion)

  # Add data to dataDict
  for row in dataCSV[1:]:
    for i, cell in enumerate(row):
      
      match = headerRegexMatch.match(headerRow[i])
      if match is None:
        continue
      
      intentVietnamese = match.group(1)
      
      intentEnglish = searchIntent(intentVietnamese)
      
      if intentEnglish:
        addData(intentEnglish, cell)
      else:
        print('[Add Data] Intent not found:', intentVietnamese)
  
  cleanDataDict()
  convertToRasaYAML()  