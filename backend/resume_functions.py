import prompter

from open_interface import ask_gpt
from hacker_news_scraper import get_jobs, scrape_web


def gap_finder(resume, job_desc):
    # Interact with chatGPT
    promt = focusAreas((job_desc, resume))
    result = ask_gpt_context(promt)

    context = promt + result
    promt = idGaps3(result)
    result = ask_gpt_context(context, promt)

    context = context + promt + result
    promt = actAdv3(result)
    result = ask_gpt_context(context, promt)
    
    path_to_file = "/backend/gaps.txt"
    with open(path_to_file, 'a') as gaps
       gaps.write(result) 

    return path_to_file
    
    


def get_recomendations(resume):
    description = ""
    for job in get_jobs(): 
        # Retrieve the job data
        if "text" in jobs.keys():
            content = jobs["text"] 
        else:
            content = scrape_web(jobs["url"]) 
