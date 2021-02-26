#!/usr/bin/env python
# coding: utf-8

# # Twitter Data Stream

# ## Install Modules

# In[ ]:


#!pip install selenium google-cloud-bigquery pyarrow


# ## Import Modules

# In[ ]:


# For accessing and parsing Twitter Webpages
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
from google.cloud import bigquery

# Structuring Collected Data
import pandas as pd

# General Libraries
import time
import datetime
import re
import os
import requests
from collections import defaultdict


# ## Variable Declarations

# In[ ]:


# Twitter Handles to be scraped
twitter_users = ['slickdeals', 'WHO', 'POTUS', 'backlon', 'instagram']

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\yashsri\Desktop\Twitter_Scraper\Twitter Data Stream.json'
bq_client = bigquery.Client()

table_id = "twitter-data-stream.twitter_data.twitter_data_values"

job_config = bigquery.LoadJobConfig(
    autodetect=True,
)


# ## Data Scrape Function

# ### Scrape Tweet IDs

# In[ ]:


def scrape_tweet_ids(user):
#Input: Twitter User Handle (String)
#Output: (Twitter ID (String), DateTime (String))

#Description: 
#- Initiate a Webdriver instance (Firefox here)
#- Store unique ID,DateTime pairs in ids (Set)
#- Load Twitter User page and added wait time for page load
#- Finds all the "a" tags in the current browser with the status_format (String)
#- Extracts datetime from the "time" tag
#- The function collects the tweets for the current date.
#- If date doesn't match with today's date, the flag becomes False and loop breaks.
#- Else, the loop continues with page scrolling.

#- Stale Element and Missing Tag errors are handled using try/except.    

    browser = webdriver.Firefox(executable_path = 'geckodriver.exe')
    time.sleep(1)
    
    ids = set()
    
    status_format = "https://twitter.com/" + user + "/status/"

    browser.get('https://twitter.com/' + user)
    time.sleep(1)
    
    flag = True

    while flag:
        
        try:
            
            a_tags = browser.find_elements_by_tag_name("a")

            for link in a_tags:

                url = link.get_attribute('href')

                if status_format in url:

                    tweet_id = url.split(status_format)[1].split("/")[0]
                    dt = link.find_elements_by_tag_name("time")
                    
                    if len(dt) > 0:
                        dt = dt[0].get_attribute("datetime")
                        
                    else:
                        continue
                    
                    #print(datetime.datetime.strptime(dt.split("T")[0], '%Y-%m-%d').date(), datetime.datetime.strptime('2021-02-25', '%Y-%m-%d').date(), datetime.datetime.strptime('2021-02-25', '%Y-%m-%d').date() != datetime.datetime.strptime(dt.split("T")[0], '%Y-%m-%d').date())

                    if datetime.datetime.strptime('2021-02-25', '%Y-%m-%d').date() != datetime.datetime.strptime(dt.split("T")[0], '%Y-%m-%d').date():
                        flag = False
                        
                    ids.add((tweet_id, dt))
                        
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            
        except Exception as error:
            
            print(error)
            continue
    
    browser.quit()
    return ids


# ### Scrape Tweet Data

# In[ ]:


def scrape_tweet_data(user, id):
#Input: Twitter User Handle (String), Tweet ID (String)
#Output: Tweet Data (Dictionary)

#Description: 
#- Initiate a Webdriver instance (Firefox here)
#- Store unique hashtags, urls, mentions (Set)
#- Load Twitter User page and added wait time for page load
#- Finds all the "a" tags in the current browser with the twitter shortening format (String)
#- Extracts data from the "span" tag with specific characters to determine hashtags and mentions. 

#- Stale Element and Missing Tag errors are handled using try/except.
    
    browser = webdriver.Firefox(executable_path = 'geckodriver.exe')
    time.sleep(1)
    
    status_format = "https://twitter.com/" + user + "/status/"
    
    data = dict()
    mentions = set()
    urls = set()
    hashtags = set()
    
    flag = True
    
    while flag:
        
        try:

            browser.get(status_format + id[0])
            time.sleep(5)

            article = browser.find_element_by_tag_name("main").find_element_by_tag_name("article")

            a_tags = article.find_elements_by_tag_name("a")

            for a in a_tags:

                link = a.get_attribute('href')

                if "https://t.co" in link:
                    urls.add(link)

            span_tags = article.find_elements_by_tag_name("span")

            body = ''
            datetime = None

            for span in span_tags[3:]:

                text = span.text.strip()

                if '@' in text:
                    mentions.add(text)

                if '#' in text:
                    hashtags.add(text)

                if '·' in text:
                    break

                body += text + " "


            data['mentions_list'] = str(list(mentions))
            data['urls_list'] = str(list(urls))
            data['hashtags_list'] = str(list(hashtags))
            data['tweet_id'] = id[0]
            data['username'] = user
            data['date'] = id[1].split("T")[0].strip()
            data['time'] = id[1].split("T")[1].split(".")[0]
            data['tweet_body'] = body.strip()
            
            flag = False
            
        except Exception as error:
            
            print(error)
            continue
    
    browser.quit()
    return data


# ## Driver Function

# ### Scrape Twitter User Data

# In[ ]:


data = pd.DataFrame()

for user in twitter_users:
    
    ids = scrape_tweet_ids(user)
    
    for id in ids:
        data = data.append(scrape_tweet_data(user, id), ignore_index = True)


# ### Save DataFrame to BigQuery

# In[ ]:


job = bq_client.load_table_from_dataframe(
    data, table_id, job_config=job_config
)
job.result()

table = bq_client.get_table(table_id)
print(
    "Loaded {} rows and {} columns to {}".format(
        table.num_rows, len(table.schema), table_id
    )
)

