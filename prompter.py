## Different prompts to be fed into Llama to generate the comparisons
prompts = [
    'Given the following job posting and a candidate''s resume, identify the key requirements for the role. Extract relevant information from the resume and compare it with the job posting to identify skills gaps. Prioritize the identified gaps and provide actionable advice for the candidate on how to address them, considering factors such as acquiring certifications or gaining additional experience. Present the results in a clear and concise format. ',
    'Given this job posting, identify and list the key requirements and qualifications mentioned, including skills, experience, education, and any specific certifications or qualifications. Provide a concise summary of the essential criteria for the role: ',
    'Now, analyze the attached resume and extract relevant information, including skills, experience, education, and certifications. Pay attention to details such as job titles, years of experience, and specific achievements. Provide a summarized overview of the candidate''s qualifications.: ',
    'Compare the information extracted from the resume with the key requirements identified in the job posting. Highlight any matches and mismatches in terms of skills, experience, education, and certifications. Present the comparison results in a clear format. ',
    'Based on the comparison results, identify and list the skills gaps between the candidate''s resume and the job posting. Pinpoint areas where the candidate may be have room for improvement in required skills, experience, or qualifications. ',
    'Generate actionable advice for the job applicant to address the identified skills gaps. Suggest specific steps the candidate can take, such as acquiring relevant certifications, gaining additional experience, or highlighting transferable skills. Offer clear and practical recommendations. ',
    'Now, sort the identified skills gaps and advice and assign a priority, based on their impact on the candidate''s suitability for the job role. Consider which gaps are critical for success in the position and should be addressed first. Provide a ranked list of recommendations. ',
    'Present the comparison results, skills gaps where they do exist, and prioritized recommendations in a clear and concise format. Use language that is easy for the candidate to understand, and provide specific examples or suggestions for improvement. ',
    'Analyze the following job posting and attached resume. Identify key skills mentioned in the job posting, compare the applicant''s job history with the job requirements, and assess how well the applicant''s education aligns with the position. Provide insights into the relevance of experiences and qualifications.',
    'Given the mentioned job posting and resume, as well as the following focus areas, match the skills mentioned in the job posting with those on the resume. Identify any gaps in the applicant''s skills based on the job requirements. Additionally, assess if the applicant''s past experiences cover the required tasks and responsibilities, pinpointing areas where the experience falls short.',
    'Provide actionable advice based on the job posting and the applicant''s resume. Identify and emphasize the applicant''s strengths and experiences that align well with the job posting. Offer constructive suggestions for addressing identified skills and experience gaps. Additionally, recommend specific courses, certifications, or resume optimization strategies to enhance the applicant''s chances.'
]

def onePrompt(jobPost_resume):
    # Tries to get everything from just one prompt
    
    return prompts[0] + "\n\n<Job Post>" + jobPost_resume[0] + "\n<Job Post/> " + "\n\n<Resume>" + jobPost_resume[1] + "\n<Resume/>"

def xtractReqs(jobPost):
    # Step 1
    # Gives the entire text from the job post and prompts the LLM
    # into extracting the requirements
    
    return prompts[1] + "\n\n<Job Post>" + jobPost[0] + "\n<Job Post/>"

def xtractResume(resume):
    # Step 2
    # Gives the entire text from the job post and prompts the LLM
    # into extracting the requirements
    
    return prompts[2] + "\n\n<Resume>" + resume[0] + "\n<Resume/>"

def compare(reqs_info):
    # Step 3
    # Compares the requirements with the resume and prompts the LLM
    # into generating a comparison
    print(reqs_info)
    
    return prompts[3] + "\n\n<Requirements>" + reqs_info[0] + "\n<Requirements/> " + "\n\n<Info>" + reqs_info[1] + "\n<Info/>"

def gaps(comps):
    # Step 4
    # Uses the previous comparison to identify skills gaps
    
    return prompts[4] + "\n\n<Comparison>" + comps[0] + "\n<Comparison/>"

def advice(gaps):
    # Step 5
    # Gives advice based on identified gaps
    
    return prompts[5] + "\n\n<Gaps>" + gaps[0] + "\n<Gaps/>"

def prioritize(gaps_advice):
    # Step 6
    # Prioritizes the advice based on the identified gaps
    
    return prompts[6] + "\n\n<Gaps>" + gaps_advice[0] + "\n<Gaps/> " + "\n\n<Advice>" + gaps_advice[1] + "\n<Advice/>"

def summarize(comp_gaps_ranked):
    # Step 7
    # Summarizes the prioritized advice
    
    input = "\n\n<Comparison>" + comp_gaps_ranked[0] + "\n<Comparison/> " + "\n<Gaps>" + comp_gaps_ranked[1] + "\n\n<Gaps/> " + "\n<Ranked>" + comp_gaps_ranked[2] + "\n<Ranked/>"
    
    return prompts[7] + input

# For 3-prompt architecture
def focusAreas(jobPost_resume):

    return prompts[8] + "\n\n<Job Post>" + jobPost_resume[0] + "\n<Job Post/> " + "\n\n<Resume>" + jobPost_resume[1] + "\n<Resume/>"

def idGaps3(areas):

    return prompts[9] + "\n\n<Areas>" + areas[0] + "\n<Areas/>"

def actAdv3(jobPost_resume_gaps):

    return prompts[10]  + "\n\n<Job Post>" + jobPost_resume_gaps[0] + "\n<Job Post/> " + "\n\n<Resume>" + jobPost_resume_gaps[1] + "\n<Resume/>" + "\n\n<Gaps>" + jobPost_resume_gaps[2] + "\n<Gaps/>"