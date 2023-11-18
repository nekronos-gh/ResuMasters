import prompter
from open_interface import ask_gpt, ask_gpt_context
from hacker_news_scraper import get_jobs, scrape_web


def gap_finder(resume, job_desc):
    # Interact with chatGPT
    promt = prompter.focusAreas((job_desc, resume))
    result = ask_gpt_context(promt)

    context = promt + result
    promt = prompter.idGaps3(result)
    result = ask_gpt_context(context, promt)

    context = context + promt + result
    promt = prompter.actAdv3(result)
    result = ask_gpt_context(context, promt)
    
    path_to_file = "/backend/gaps.txt"
    with open(path_to_file, 'a') as gaps:
       gaps.write(result) 

    return path_to_file
    
    


def get_recommendations(resume):
    description = ""
    for job in get_jobs(): 
        # Retrieve the job data
        result = {}
        if "text" in job.keys():
            content = job["text"] 
        elif "url" in job.keys():
            content = scrape_web(job["url"]) 
        else:
            continue
        if prompter.match((resume, content)) == "TRUE":
            description = ask_gpt(f"Please provide me with a description of the following job data: {content}") 
            yield {
                "url": job["url"] if "url" in job.keys() else None,
                "description": description,
            }
