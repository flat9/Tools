import requests
from lxml import etree
import sys

if len(sys.argv) != 2:
  print 'Please Enter URL'
else:
  fp = open('result.txt','a')
  fp.write(sys.argv[1] + '\n')
  search_url = 'https://dns.aizhan.com/' + sys.argv[1] + '/'
  r = requests.get(search_url)
  select = etree.HTML(r.content)
  counts = select.xpath('//body/div[4]/div[2]/ul/li[4]/span/text()')
  print '====================='
  print 'Counts:' + counts[0]
  print '====================='
  for i in range(1,(int(counts[0])-1)/20 + 2):
    search_url = 'https://dns.aizhan.com/' + sys.argv[1] + '/' + str(i) + '/'
    r = requests.get(search_url)
    select = etree.HTML(r.content)
    urls = select.xpath('//body/div[@class="dns-wrap"]/div[@class="dns-content"]/table/tbody/tr[*]/td[2]/a/text()') 
    for url in urls:
      print url
      fp.write(url + '\n')
      flag = raw_input('Next Page[n]:')
      if flag == 'n':
        continue
      else:
        fp.close()
        exit()
  fp.close()

