#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system(' pip install requests')
get_ipython().system('pip install beautifulsoup4')


# In[37]:


import os
os.getcwd()


# In[38]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[53]:



def create_links(url,rent_type, numpages,listoflinks):
    for i in range (numpages):
        listoflinks.append(url+'page='+str(i)+'&'+rent_type)
    return listoflinks
   

    


# In[54]:


url= 'https://www.uniplaces.com/accommodation/lisbon?'
rent_type='rent-type[]=unit'
urlist=list()


# In[55]:


texts=list()
def get_html(inlist,outlist ):
    for url in inlist:
        x=requests.get(url)
        text=BeautifulSoup(x.content, 'html.parser')
        outlist.append(text)
    return(outlist)

    
    
    


# In[56]:



def get_links(inlist, outlist):
    for text in inlist:
        x=text.find_all('a', {'class':"sc-q9wvaw-0 goZTpP"}, recursive=True)
        for link in x:
            outlist.append(link.get('href'))
    return(outlist)
    

   


# In[57]:


from selenium import webdriver
import time


def get_info_sel(inlist,outframe,attr_list,identifier_list,base):
    driver = webdriver.Chrome()
    to_append=list()
    links=list(base['url'])
    for link in inlist:
        if link not in links:
            
            try:
                driver.get(link)
                time.sleep(3)
                to_append.append(str(link))
            finally:
                for i in range(len(attr_list)):
                    identifier=list(features_id.values())[i]
                    attr=list(features_attr.values())[i]
                    try:
                        element=driver.page_source
                    finally:
                        soup = BeautifulSoup(element)
                        text=soup.find(attr,identifier)
                        if text is not None:
                            value = text.get_text()
                            to_append.append(value)
                        else:
                             to_append.append('NA')
                        if len(to_append)==len(outframe.columns):  
                            outframe_length = len(outframe)
                            outframe.loc[outframe_length] = to_append
                            to_append.clear()
                        else:
                            pass
                else:
                    pass
               
               
    return outframe
       
    


# In[58]:


url= 'https://www.uniplaces.com/accommodation/lisbon?'
rent_type='rent-type[]=unit'
features_id={'headers':{'class':"header__title"}, 'price':{'class':'booking-box__value'},'type_room':{'class':"header__icon__label"},'number_rooms': {'class':'header__icon__label'},'neighbourhood':{'neighbourhood__card neighbourhood__card--left'}}
features_attr={'headers':'h1', 'price':'span','type_room':'div','number_rooms':'span','neighbourhood':'h3'}
def create_df(url, rent_type,features_id,features_attr,base):
    urlist=list()
    n=int(input('Number of pages to be scrapped'))
    links_pages=create_links(url,rent_type,n,urlist)
    texts=list()
    page_html=get_html(links_pages, texts)
    links_by_room=list()
    roomslinks=get_links(texts, links_by_room)
    columns_list=[]
    columns_list.append('url')
    for i in range(len(features_id)):
        x=list(features_id)[i]
        columns_list.append(x)          
    df = pd.DataFrame(columns=columns_list)
    df=get_info_sel(roomslinks,df,features_attr,features_id,base)
    return df, columns_list
        
        
    
    
    
    
    
    


# In[59]:


import sqlite3
def create_base():
    con = sqlite3.connect('example.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE rooms
                   ('url' PRIMARY KEY, 'headers' text, 'price' text, 'type_room' text,'number_rooms' text, 'neighbourhood' text )''')
    con.commit()
    con.close()


# In[60]:


def update_base(df,columns_list):
    con = sqlite3.connect('example.db')
    cur = con.cursor()
    cols=list()
    cols_str='","'.join([str(n) for n in columns_list])
    values=[]
    for row in df.itertuples():
        row_list=[]
        for element in row:
            row_list.append(element)
        for i in range(len(columns_list)):
            values.append(str(row_list[i]))
    
        sql = "INSERT INTO rooms ("'"'+cols_str+'"'") VALUES(?,?,?,?,?,?);"
        cur.execute(sql,values)
        con.commit()
        values=[]


# In[61]:


def download_base():
    con = sqlite3.connect('example.db')
    cur = con.cursor()
    sql_query= 'SELECT * FROM rooms'
    base=pd.read_sql(sql_query,con)
    return base


# In[62]:


def main():
    try:
        create_base()
    except TypeError:
        print('table rooms already exists')
    finally:
        base=download_base()
        df, columns_list=create_df(url, rent_type,features_id,features_attr,base)
        update_base(df,columns_list)

