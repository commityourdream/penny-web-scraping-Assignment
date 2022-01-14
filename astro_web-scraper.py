#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import pandas as pd
import requests
import re


# In[2]:


read_file = pd.read_excel ("Dataset - Penny test.xlsx")


# In[3]:


read_file.to_csv ("Dataset_Penny_test.csv",index = None,header=True)


# In[4]:


df = pd.DataFrame(pd.read_csv("Dataset_Penny_test.csv"))


# In[5]:


df.head()


# In[6]:


df1 = df['Identifier']
df1=df1[1:8]


# # To Scrape Product_url

# In[7]:


product_urls = []
for i in range(0,1):
    url=df['Identifier'].iloc[i].format(1)
    #print(url)
    req=requests.get(url)
    soup = BeautifulSoup(req.text, "html5lib")
    parent_class = soup.find_all("div",class_="dswc_item_wrapper swiper-slide")
    for purl in parent_class:
        product_url = purl.find("a")
        #print(product_url['href'])
        product_url = product_url['href']
        prod_url_dict = {'product_url':product_url}
        product_urls.append(prod_url_dict)  


# # To Scrape Product_Details

# In[ ]:


astro_data=[]
product_urls_data = pd.DataFrame(product_urls)
for i in range(len(product_urls_data)):
    product_urll=product_urls_data['product_url'].iloc[i].format(1)
    request=requests.get(product_urll)
    soup = BeautifulSoup(request.text, "html5lib")
    parent = soup.find_all("div",{"class":"et_pb_row et_pb_row_1_tb_body"})
    for p in parent:
        product_name = p.find("h1")       
        if product_name:
            product_name=product_name.text
        else:
            product_name=None
            
        product_specs = p.find_all("div",{"class":"et_pb_tab_content"})[1]

        if product_specs:
            product_specs=product_specs.text.replace('\n','').replace('\t','')
        else:
            product_specs=None
            
        product_img = p.find("img",{"class":"wp-post-image"})

        if product_img:
            product_img=product_img['data-large_image']
        else:
            product_img=None
            
        sku = p.find("span",{"class":"sku"})

        if sku:
            sku=sku.text
        else:
            sku=None
            
        product_cat = p.find("span",{"class":"posted_in"})
        
        if product_cat:
            product_cat=product_cat.text
        else:
            product_cat=None
        
        source = {'source':'Astro Website',
                  'product_name':product_name,
                  'product_category':product_cat,
                  'SKU':sku,
                  'product_specifications':product_specs,
                  'product_url':product_urll,
                  'product_image_url':product_img
                 }
        astro_data.append(source)
            
        


# In[ ]:


Data=pd.DataFrame(astro_data)


# In[ ]:


Data


# In[ ]:


Data.to_csv('astro_product_details.csv',index=False)


# In[ ]:




