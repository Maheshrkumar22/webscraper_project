import pandas as pd
import numpy as np
from requests_html import AsyncHTMLSession
import asyncio
import aiohttp
import json,re,jsonify 
import asyncio,itertools

import requests
from bs4 import BeautifulSoup

async def scrape_page(url):
    # Initialize session
    session = AsyncHTMLSession()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:143.0) Gecko/20100101 Firefox/143.0',
               'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Referer': 'https://www.google.com/',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'cross-site',
                'Sec-Fetch-User': '?1',
              }

    
    # Load page and render JS
    response = await session.get(url,headers=headers)
    await response.html.arender(timeout=20, sleep=2)  # Render JS, wait 2s post-render
    
    if response.status_code!=200:
      print(f"The request failed with an error {response.status_code}. The Python scraping bot is being blocked by the website security")

    # Parse with BeautifulSoup
    soup = BeautifulSoup(response.html.html, 'html.parser')

    await session.close() # Close the session

    return soup,response.status_code

def remove_multiple_chars(text, chars_to_remove):
    for char in chars_to_remove:
        text = text.replace(char, ' ')
    return text



def scrape_data(source_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(source_url, headers=headers)

    html_content = response.text

    soup = BeautifulSoup(html_content, "lxml")

    if(soup.find_all(["a","p","h1","h2","h3","h4","h5"])==[]):
    # Run the async function
        soup,response.status_code = asyncio.run( scrape_page(source_url))
        if(response.status_code!= 200):
            data = {{
            "Name":"Data Not Found",
            "Designation":"Bot been blocked",
            "img url":None
            }}
            return jsonify(data)

    ############# scrape and save relevant tags
    h1 = [str(x.get_text().strip()) for x in soup.find_all(['h1'])]
    h1 = list(filter(None, h1))

    h2 = [str(x.get_text().strip()) for x in soup.find_all(['h2'])]
    h2 = list(filter(None, h2))

    h3 = [str(x.get_text().strip()) for x in soup.find_all(['h3'])]
    h3 = list(filter(None, h3))

    h4 = [str(x.get_text().strip()) for x in soup.find_all(['h4'])]
    h4 = list(filter(None, h4))

    h5 = [str(x.get_text().strip()) for x in soup.find_all(['h5'])]
    h5 = list(filter(None, h5))

    h6 = [str(x.get_text().strip()) for x in soup.find_all(['h6'])]
    h6 = list(filter(None, h6))

    p = [str(x.get_text().strip()) for x in soup.find_all(['p'])]
    p = list(filter(None, p))

    a = [str(x.get_text().strip()) for x in soup.find_all(['a'])]
    a = list(filter(None, a))

    div = [str(x.get_text().strip()) for x in soup.find_all(['div'])]
    div = list(filter(None, div))

    span = [str(x.get_text().strip()) for x in soup.find_all(['span'])]
    span = list(filter(None, span))

    strong = [str(x.get_text().strip()) for x in soup.find_all(['strong'])]
    strong = list(filter(None, strong))


    ######################
    include_a_tag_flag=False

    text = source_url
    pattern = r"google|mathco|salesforce"
    include_a_tag_flag=bool(re.findall(pattern, text))

    lists = [h1, h2, h3, h4, h5, h6, p, span]
    lists_name=['h1','h2','h3','h4','h5','h6','p', 'span']
    if(include_a_tag_flag):
        lists.append(a)
    lists_name.append('a')

    ############# Keywords to search
    keywords = ['officer', 'chief', 'ceo', 'partner', 'president','founder']
    pattern = re.compile(r'\b(' + '|'.join(keywords) + r')\b', re.IGNORECASE)

    # Count matches per list
    results = []
    for i, lst in enumerate(lists, 1):
        text = ' '.join(lst).lower()
        matches = pattern.findall(text)
        results.append({
            'list_index': i-1,
            'list_name': f'h{i}',
            'weightage': len(matches)
        })

    # Find list with max weightage
    max_result = max(results, key=lambda x: x['weightage'])
    print(results)
    designation_list = lists[max_result['list_index']]
    print(designation_list)
    print('Designation lists are at list: ',lists_name[max_result['list_index']],' /weightage :', max_result['weightage'])


    ############ name list ---------> Keywords to search
    lists = [h1, h2, h3, h4, h5, h6]
    lists_name=['h1','h2','h3','h4','h5','h6']
    if(include_a_tag_flag):
        lists.append(a)
        lists_name.append('a')

    name_pattern = re.compile(r'^[A-Za-z]+([- ][A-Za-z]+)*$', re.IGNORECASE)

    name_pattern = re.compile(r"^(?:[A-Z][a-z]*(?:['.-][A-Z][a-z]*)*\s*){2,4}$")

    #name_pattern = re.compile(r"^(?:[A-Z][\w\s.'-]*){2,4}$", re.UNICODE)

    # Count matches per list
    results = []
    for i, lst in enumerate(lists, 1):
        matches = [s for s in lst if name_pattern.match(s)]
        results.append({
            'list_index': i-1,
            'list_name': f'h{i}',
            'weightage': len(matches)
        })
    filtered_data = results
    print(filtered_data)
    ############filter outlier value if the weightage is more########
    if(not include_a_tag_flag):
        filtered_data=[]
    # Step 2: Calculate Q1, Q3, and IQR using numpy
    weightages = [d['weightage'] for d in results]
    q1, q3 = np.percentile(weightages, [25, 75])
    iqr = q3 - q1

    # Step 3: Define the outlier bounds
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # Step 4: Use a list comprehension to filter out dictionaries with outlier weightages
    filtered_data = [d for d in results if lower_bound <= d['weightage'] <= 150]
    print(filtered_data)
    #############################

    # Find list with max weightage
    max_result = max(filtered_data, key=lambda x: x['weightage'])
    print(max_result)

    name_list = lists[max_result['list_index']]
    #name_list = matches
    print(name_list)
    print('Name lists are at list: ',lists_name[max_result['list_index']],' /weightage :', max_result['weightage'])

    ############### Remove the unwanted patterns -----> clean the list

    remove_list_patterns = ["follow", "download","logo","skip","news",'subscribe','start','terms','help','reserved',\
                            'into the','exceptional','capabilities','model','committed','with','every'] # Patterns to match and remove

    regex_pattern = "|".join(remove_list_patterns) 


    name_remove_list_patterns = ["follow", "download","logo","skip","news",'contact','diversity','&','connect',\
                                "press",'subscribe','start','digital','privacy','terms','help','wallet','account',\
                                'leaders','about','cloud','demo','pricing','login','free','promise','entertain',\
                                'enthusiasm','products','platform','resource','education','health','store','government','values',\
                                'analysis','source','software','microsoft','purpose','fact','policy','studies','business','corporate','speed',\
                                'life','work','services','community','generative','overview','brand','data','engineer',\
                                'consult','read','compan','join','cpg','results','logged','vision','preference','relation',\
                                'analyst','security','tech','service','intelligen','individual','learn',\
                                'partner','ecosy','social','search','compan','equity','customer','director']
    name_regex_pattern = "|".join(name_remove_list_patterns) 

    # 2. Filter the first list using a list comprehension
    designation_list = [item for item in designation_list if not re.search(regex_pattern, item,re.IGNORECASE)]
    name_list = [item for item in name_list if not re.search(name_regex_pattern, item,re.IGNORECASE)]
    #removes 3 or more digit numbers in designation list
    designation_list = [item for item in designation_list if not re.search(r'\d{3,}', item)]

    name_list = [item for item in name_list if len(item.split()) <= 4 and len(item.split()) > 1]
    name_list = [item for item in name_list if not re.search(r'\d{3,}', item)]

    ############## extract if it contains these keywords for designation
    keywords = ['officer', 'chief', 'chairman','director','ceo','partner','president','founder','cfo','fellow','vp','senior','cto','lead']

    designation_list = [title for title in designation_list if any(keyword in title.lower() for keyword in keywords)]

    ############## -> remove unicodes
    unicode_chars_to_remove = ['\u200b', '\u00a0','\n','\u2028']


    # Use a function to apply all replacements to a single string


    name_list = [remove_multiple_chars(name, unicode_chars_to_remove) for name in name_list]
    designation_list = [remove_multiple_chars(name, unicode_chars_to_remove) for name in designation_list]
    
    #####remove reduntant designation------------
    # Use filter with a lambda function to keep only the first occurrence of each element
    seen = set()
    designation_list = list(filter(lambda x: x not in seen and not seen.add(x), designation_list))

    #######creating a dtaframe ------

    data = {'Name': name_list, 'Designation': designation_list}

    data = list(itertools.zip_longest(name_list, designation_list))

    # Create the DataFrame, specifying column names
    df = pd.DataFrame(data,columns=['Name','Designation'])

    #############---- create new columns to clean the name and find image url
    df[['First Name', 'Last Name']] = df['Name'].str.split(n=1, expand=True)

    # Convert the new columns to lowercase
    df['First Name'] = df['First Name'].str.lower()
    df['Last Name'] = df['Last Name'].str.lower()

    ### find image source

    img_tags = soup.find_all('img')
    src_list = [img['src'] for img in img_tags if 'src' in img.attrs]                   #appending some image list present in src tag
    data_src_list = [img['data-src'] for img in img_tags if 'data-src' in img.attrs]    #appending some image list present in data-src tag

    src_list.extend(data_src_list)

    ##### map in the dataframe

    df['img url']=None
    for index, row in df.iterrows():
        first_name = row['First Name']
        last_name = row['Last Name']

        # Check if the first name is present in any of the URLs
        for url in src_list:
            # Convert both name and URL to lowercase for case-insensitive matching
            if first_name is not None and first_name in str(url).lower():
                # If a match is found, assign the full URL to the new column
                df.at[index, 'img url'] = url
                # Break the inner loop once a match is found
                break
        for url in src_list:
            # Convert both name and URL to lowercase for case-insensitive matching
            if last_name is not None and last_name in str(url).lower():
                # If a match is found, assign the full URL to the new column
                df.at[index, 'img url'] = url
                # Break the inner loop once a match is found
                break

    ########find if url has direct link or append

    full_url_flag = False 
    if(((str(df['img url'][1])[:8]) or (str(df['img url'][0])[:8]) or (str(df['img url'][-1])[:8])) == 'https://'):
        full_url_flag = True
    ######append stripped url if direct link is not found
    stripped_url = source_url[:source_url.find('.com') + len('.com')]

    if(not full_url_flag):
        df['img url']=stripped_url+df['img url']

    df.loc[df['img url'].duplicated(keep='first'), 'img url'] = None

    df.drop(columns=['First Name','Last Name'],inplace=True)

    ###fill null values

    df['Name']=df['Name'].fillna('')
    df['Designation']=df['Designation'].fillna('')

    ###convert the value to json
    json_return = df.to_json(orient='records',indent=3)

    return json_return

if __name__ == "__main__":
    pass

   
    
   










