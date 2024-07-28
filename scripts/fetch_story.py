fileCSVURL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSAWBkVy4eZ0k04ZKEwppDMvCHNlDIxoZXn1H8puT4xqrw-ui4y-rnFRgBaImR7bBg6XGaVul1X279U/pub?gid=1426250826&single=true&output=csv'
outputName = 'data_rules_stories/stories_from_sheets.yml'

import os
import csv
import requests
import io


stories : list[list[str]] = []
currentPWD = os.path.join(os.getcwd(), '.~scripts')

def fetchDataCSVFromURL(url):
  
  response = requests.get(url)
  data = response.content.decode('utf-8')
  dataFile = io.StringIO(data)
  reader = csv.reader(dataFile)
  return [row for row in reader]
  
def convertToRasaYAML():
  with open(outputName, 'w') as file:
    
    file.write(f'version: "3.1"\n\n')
    file.write(f'stories:\n')
    
    for story in stories:
      n = 0
      file.write(f'  - intent: {story[0]}\n    steps:\n')
      n += 1
      while n < len(story):
        if n % 2 == 0:
          file.write(f'      - intent: {story[n]}\n')
        else:
          file.write(f'      - action: {story[n]}\n')
        n += 1      
      file.write('\n')



if __name__ == '__main__':
  print('Fetching data from Stories sheet...')
  dataCSV = fetchDataCSVFromURL(fileCSVURL)
  
  if (dataCSV is None):
    print('Error fetching data')
    exit(1)
  
  
  startingCol = 7
  startingRow = 3
  nameRow = 1
  
  r = startingRow
  c = startingCol
  
  try:
    while(c < len(dataCSV[r]) and dataCSV[r][c] != ''):
      story = [dataCSV[nameRow][c]]
      while(r < len(dataCSV) and dataCSV[r][c] != ''):
        if not dataCSV[r][c].isnumeric():
          print(dataCSV[r][c])
          story.append(dataCSV[r][c])
        r += 1
      if (len(story) > 1):
        stories.append(story)
      c += 1
      r = startingRow
    print('Data fetched successfully', stories)
    
  except Exception as e:
    print('Error', e, 'at', r, c)
  
  convertToRasaYAML()
  print('Data saved to', outputName)  