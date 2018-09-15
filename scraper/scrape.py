# -*- coding: utf-8 -*-


def glassdoorScrape(get_short = False):
    
    """
    Created on Tue Aug 16 22:41:30 2016
    Scrape Glassdoor website using SELENIUM
    @author: Diego De Lazzari
    """

    from selenium import webdriver
    #from bs4 import BeautifulSoup # For HTML parsing
    from time import sleep # To prevent overwhelming the server between connections
    from collections import Counter # Keep track of our term counts
    from nltk.corpus import stopwords # Filter out stopwords, such as 'the', 'or', 'and'
    import pandas as pd # For converting results to a dataframe and bar chart plots
    from selenium.webdriver.common import action_chains, keys
    from selenium.common.exceptions import NoSuchElementException
    import numpy as np
    import sys

    import pandas, csv
    my_file = 'salaries.csv'

    # call the helper
    
    from helperP3 import load_obj, save_obj, init_glassdoor, searchJobs, text_cleaner, get_pause, searchJobSalaries
    
        # 1- Load existing dictionary. Check for initial dictionary. 
        # If empty initialize
            
    try:               
        sf_links = load_obj('san_francisco_links')
        ny_links = load_obj('new_york_links')
        wa_links = load_obj('washington_links')
        detriot_links = load_obj('detriot_links')
        austin_links = load_obj('austin_links')
        boston_links = load_obj('boston_links')
        los_angeles_links = load_obj('los_angeles_links')

    except:
        save_obj([], 'san_francisco_links')
        save_obj([], 'new_york_links')
        save_obj([], 'washington_links')
        save_obj([], 'detriot_links')
        save_obj([], 'austin_links')
        save_obj([], 'boston_links')
        save_obj([], 'los_angeles_links')
        
        sf_links = load_obj('san_francisco_links')
        ny_links = load_obj('new_york_links')
        wa_links = load_obj('washington_links')
        detriot_links = load_obj('detriot_links')
        austin_links = load_obj('austin_links')
        boston_links = load_obj('boston_links')
        los_angeles_links = load_obj('los_angeles_links')
    
#       2- Choose what you want to do: 
#       get_shot => Scraping for links, 
#       get_long => Scraping for data,


#       3- initialize website, cities and jobs
        
    website = "https://www.glassdoor.com/index.htm"
        
    job_name_list= ['Software Engineer', 'Data Scientist', 'QA Engineer']
    city_list = ['San Francisco','Detroit','Washington','Austin','Boston','Los Angeles']
    city_links = ['san_francisco_links', 'new_york_links', 'washington_links', 'detriot_links', 'austin_links', 'boston_links', 'los_angeles_links']
    links = [sf_links, ny_links, wa_links, detriot_links, austin_links, boston_links, los_angeles_links]

#       Initialize the webdriver
        
    browser = init_glassdoor()  

#       4- Scrape the short list or the links (when you ae done, both are false)
            
#       search for jobs (short description) 
#    for job_name in job_name_list:
#        for index, city in enumerate(city_list):
#            try:    
#                browser.get(website)
#                update_link = searchJobs(job_name, city, links[index], browser)
#            except Exception as e:
#                print(e)
#            
#            save_obj(update_link, city_links[index])
                    
    for index, link in enumerate(links):
        while len(link) > 0:
            rnd_job = np.random.choice(range(len(link)))
            try:
                
                ids = link[rnd_job][0]
                page = link[rnd_job][1]
    
                print(page)
                    
                browser.get(page)                 
                sleep(2)

                    
                # Extract text   //*[@id="JobDescContainer"]/div[1]
                desc_list = browser.find_element_by_xpath('//*[@id="JobDescriptionContainer"]/div[1]').text
                description = text_cleaner(desc_list)

                salary = browser.find_element_by_xpath('//div[@id="salWrap"]/h2').text
                title = browser.find_element_by_xpath('//h2[@class="noMargTop margBotXs strong"]').text
                company = browser.find_element_by_xpath('//span[@class="strong ib"]').text
                location = browser.find_element_by_xpath('//span[@class="subtle ib"]').text[3:]

                payload = {"company": company, "location": location, "title": title, "salary": salary}
                with open('salaries.csv', 'a') as f:  # Just use 'w' mode in 3.x
                    w = csv.DictWriter(f, payload.keys(), quoting = csv.QUOTE_ALL)
                    w.writerow(payload)
                print(payload)
                    
                dummy=link.pop(rnd_job)
                               
                # if everything is fine, save
                save_obj(link, city_links[index])
                
                print 'Scraped successfully ' + ids
                
                sleep(get_pause())
            except Exception as e:   
                print (e)
                print ids + ' is not working! Skipping.'
                print 'Still missing ' + str(len(link)) + ' links' 
                dummy=link.pop(rnd_job)
                sleep(8)
                
    browser.close()

glassdoorScrape(False)
