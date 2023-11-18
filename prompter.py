## Different prompts to be fed into Llama to generate the comparisons
def onePrompt(jobPost_resume):
    # Tries to get everything from just one prompt
    prompt = """Given the following job posting and a candidate's resume, 
        identify the key requirements for the role. Extract relevant 
        information from the resume and compare it with the job posting 
        to identify skills gaps. Prioritize the identified gaps and provide 
        actionable advice for the candidate on how to address them, considering 
        factors such as acquiring certifications or gaining additional 
        experience. Present the results in a clear and concise format. """
    
    return prompt + "<Job Post>" + jobPost_resume[0] + "<Job Post/> " + "<Resume>" + jobPost_resume[1] + "<Resume/>"

def xtractReqs(jobPost):
    # Step 1
    # Gives the entire text from the job post and prompts the LLM
    # into extracting the requirements
    prompt = """Given this job posting, identify and list 
        the key requirements and qualifications mentioned, including 
        skills, experience, education, and any specific certifications 
        or qualifications. Provide a concise summary of the essential 
        criteria for the role: """
    
    return prompt + "<Job Post>" + jobPost[0] + "<Job Post/>"

def xtractResume(resume):
    # Step 2
    # Gives the entire text from the job post and prompts the LLM
    # into extracting the requirements
    prompt = """Analyze the attached resume and extract relevant 
        information, including skills, experience, education, and 
        certifications. Pay attention to details such as job titles, 
        years of experience, and specific achievements. Provide a 
        summarized overview of the candidate's qualifications.: """
    
    return prompt + "<Resume>" + resume[0] + "<Resume/>"

def compare(reqs_info):
    # Step 3
    # Compares the requirements with the resume and prompts the LLM
    # into generating a comparison
    prompt = """Compare the information extracted from the resume with
         the key requirements identified in the job posting. Highlight 
        any matches and mismatches in terms of skills, experience, 
        education, and certifications. Present the comparison results 
        in a clear format. """
    
    return prompt + "<Requirements>" + reqs_info[0] + "<Requirements/> " + "<Info>" + reqs_info[1] + "<Info/>"

def gaps(comps):
    # Step 4
    # Uses the previous comparison to identify skills gaps
    prompt = """Based on the comparison results, identify and list the 
        skills gaps between the candidate's resume and the job posting. 
        Pinpoint areas where the candidate may be have room for 
        improvement in required skills, experience, or qualifications. """
    
    return prompt + "<Comparison>" + comps[0] + "<Comparison/>"

def advice(gaps):
    # Step 5
    # Gives advice based on identified gaps
    prompt = """Generate actionable advice for the job applicant to 
        address the identified skills gaps. Suggest specific steps the 
        candidate can take, such as acquiring relevant certifications, 
        gaining additional experience, or highlighting transferable 
        skills. Offer clear and practical recommendations. """
    
    return prompt + "<Gaps>" + gaps[0] + "<Gaps/>"

def prioritize(gaps_advice):
    # Step 6
    # Prioritizes the advice based on the identified gaps
    prompt = """Prioritize the identified skills gaps and advice based 
        on their impact on the candidate's suitability for the job 
        role. Consider which gaps are critical for success in the position 
        and should be addressed first. Provide a ranked list of 
        recommendations. """
    
    return prompt + "<Gaps>" + gaps_advice[0] + "<Gaps/> " + "<Advice>" + gaps_advice[1] + "<Advice/>"

def summarize(comp_gaps_ranked):
    # Step 7
    # Summarizes the prioritized advice
    prompt = """Present the comparison results, skills gaps, and 
        prioritized recommendations in a clear and concise format. Use 
        language that is easy for the candidate to understand, and provide 
        specific examples or suggestions for improvement. """
    
    input = "<Comparison>" + comp_gaps_ranked[0] + "<Comparison/> " + "<Gaps>" + comp_gaps_ranked[1] + "<Gaps/> " + "<Ranked>" + comp_gaps_ranked[2] + "<Ranked/>"
    
    return prompt + input