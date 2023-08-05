# -*- coding: utf-8 -*-
#  George Gorbunov

#---------------------------------------------------------------------------------

import argparse
import datetime
import time # to calculate  elapsed time 
from time import sleep
import smtplib
from email.mime.text import MIMEText
import MySQLdb
import urllib2
from bs4 import BeautifulSoup as Broth
import re
import ConfigParser
import io
from urlparse import urljoin

graph = []

def retrieve_url (url):

   """
    To retrive the contents of url .
    The url must be in some valid format :
         * http://www.example.com/.
         * https://www.example.com/  """


   opener = urllib2.build_opener ()    
   try:
        t = opener.open (url).read ()
        parser = Broth(t)
        l =[x['href'] for x in parser.findAll ('a') \
                if x.has_attr ('href')]
        return l
   except urllib2.URLError:
      print ("Error accessing URL. Check your Internet connection")
      return []
   except ValueError:
        return []

def start_greeting():
    """Print some messages about this crawler"""
    print "Web-spider  for the 2017"
    print "George Gorbunov, email: gorbunov@gmail.com"
    print " let start crawling "
def summary(depth,end,start):
    """ Print summary messages  and calculate the elapsed time """
    elapsed = end - start
    elapsed_time_int = int(elapsed)
    print "-----------------------------------------------------"
    print " '*' indicated to the level depth"
    print (" %s Webpages were crawled " % (len(graph)))
    print ' Time taken for crawling {} level is :{} seconds ' \
                              .format (depth,elapsed_time_int)
    print "Done :D "

def print_links (url,n, m, db, search):
    """  to make loop to and extract the url in the crawling depth   """
    page_counter = 0
    if n == 0:
        return ""
    if [url] in graph: 
        return ""
    else:
        graph.append([url])
        
    print " %s %s " % ("*"*n,url)
    enlaces = retrieve_url (url)

    opener = urllib2.build_opener ()    
    try:
        t = opener.open (url).read ()
        parser = Broth(t)
        for x in parser.findAll ('h2'):  
            if re.search(search,x.get_text()): 
    			cursor = db.cursor()
       			sql = """INSERT INTO Headers(Date, Header, Url) VALUES ('%(Date)s', '%(Header)s', '%(Url)s') """%{"Date":datetime.date.today(), "Header":x.get_text(), "Url":url}
       
    			cursor.execute(sql)

    			db.commit()                
        
    except urllib2.URLError:
        print ("Error accessing URL. Check your Internet connection")
        return ""
    except ValueError:
        return ""

    if n != 1:
        for l in enlaces:
            l = urljoin(url, l)
            #print " %s %s " % ("*"*n,l)  
            #m = m + " %s %s \r\n" % ("*"*n,l)
            #m = m + str(
            print_links (l,n-1, m,db, search)
            page_counter +=1  # to count number of pages crawled  in the 
    #print (" %s Webpages were crawled " % (page_counter))
    return m
 
     
def main():
    while True :
        # Load the configuration file
        with open("config.ini") as f:
            sample_config = f.read()
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.readfp(io.BytesIO(sample_config))

        graph = []
        start = time.time()  #to start calculate the elapsed time 
       
        
        parser = argparse.ArgumentParser ( description = 'This application is for crawling the web page ! '\
                                                 ,version ='0.1')

        #parser.add_argument ( '-n' , '--number-of-levels' , type = int ,help = 'how deep the crawler will go')

        #parser.add_argument ('url', nargs=1,help= 'Target URL to crawle ' )

        args = parser.parse_args ()
        depth = config.getint('Miscellaneous','depth')
        #depth = args.number_of_levels
        #url =args.url[0]
        urls = config.get('Main','website')
        urls = urls.split(',')
       
        print "Websites to search: %s" % urls
        db = MySQLdb.connect(host=config.get('MySQL','MySQL_Server'), user=config.get('MySQL','MySQL_login'), passwd=config.get('MySQL','MySQL_password'), db="Headers", charset='utf8')
       
        search = config.get('Main','criteria')

        start_greeting()        # calling the function greeting
        mg = 'Web-spider report\r\n '
        for i,url in enumerate(urls):
            url = url.strip('""[]')
            print(url)
            mg = mg + print_links(url, depth, "", db, search)  # calling the function print_links
        db.close()
        
        msg = MIMEText( mg )
        end = time.time()       #"to end calculate the elapsed time "
        summary(depth,end,start)# calling the function summary


       
        msg['Subject'] = 'Crawler report '
        msg['From'] = config.get('Email','SMTP_login')
        msg['To'] = config.get('Email','SMTP_addressant')

        s = smtplib.SMTP(config.get('Email','SMTP_Server'))
        s.login(config.get('Email','SMTP_login'),config.get('Email','SMTP_password'))
        s.sendmail(config.get('Email','SMTP_login'),[config.get('Email','SMTP_addressant')], msg.as_string())
        s.quit()
        sleep(config.getint('Miscellaneous', 'time_Interval')*3600)
if __name__=='__main__':
       main ()
"""Main module."""
