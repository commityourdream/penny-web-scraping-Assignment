#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


# # To Scrape Product_url

# In[ ]:


knipex_prod_url = []
for i in range(0,40):
    url = 'https://www.knipex.com/products?&page={}'.format(i)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html5lib")
    parent = soup.find_all("div",{"class":"knipex-product-element"})
    for url in parent:
        span = url.find("span",{"class":"field-content"})
        purl = span.find('a')
        purl = 'https://www.knipex.com'+ purl['href']
        knipex_dict = {'product_url':purl}
        knipex_prod_url.append(knipex_dict)    
        
 


# In[ ]:


Data=pd.DataFrame(knipex_prod_url)
Data


# In[ ]:


Data.drop_duplicates(keep=False, inplace=True)
Data.to_csv('knipex_product_urls.csv',index=False)


# # To_Scrape_Product_Details

# In[ ]:


knipex_prod_details=[]
product_url= pd.read_csv('knipex_product_urls.csv')
#product_url
for i in range(len(product_url)):
    url=product_url['product_url'].iloc[i].format(1)
    print(url)
    r=requests.get(url)
    print(r.status_code)
    soup = BeautifulSoup(r.text, "html5lib")
    parent = soup.find_all("article",{"class":"ProductContainer"})
    #print(parent)
    for p in parent:
        product_name = p.find("div",{"class":"computed_detail_title_name"})
        if product_name:
                product_name=product_name.text
        else:
            product_name=None
            
        product_specs = p.find("div",{"class":"bulletpoint-container"})
        if product_specs:
                product_specs=product_specs.text.strip()
        else:
            product_specs=None
            
        prod_cat = soup.find("div",{"id":"block-breadcrumbs"})
        if prod_cat:
                prod_cat=prod_cat.text.split('  ')
                prod_cat = prod_cat[8]
        else:
            prod_cat=None
            
        prod_image = p.find("div",{"class":"field__item"})
        p_image = prod_image.find("img")['src']
        if p_image:
            p_image = 'https://www.knipex.com'+p_image
        else:
            p_image =None
            
#         technical_details = p.find_all("div",{"class":"key-value-class-item"})
#         #print(technical_details.strip())
#         for td in technical_details:
#             tech_det = td.text.replace(u'\xa0', u' ')
            
        knipex_dict_prod={'product_Category':prod_cat,
                          'product_name':product_name,
                          'product_url':url,
                          'product_image':p_image,
                          'product_specifications':product_specs
                         }
        
        knipex_prod_details.append(knipex_dict_prod)      


# In[ ]:


prod_details_Data=pd.DataFrame(knipex_prod_details)
prod_details_Data


# In[ ]:


prod_details_Data.to_csv('knipex_prod_details.csv',index=False)

