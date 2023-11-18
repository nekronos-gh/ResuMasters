## Different prompts to be fed into Llama to generate the comparisons
prompts = [
    'Analyze the following job posting and attached resume. Identify key skills mentioned in the job posting, compare the applicant''s job history with the job requirements, and assess to what extent the applicant''s education aligns with the position. Provide insights into how relevant relevant the applicant''s experiences and qualifications are.',
    'Given the mentioned job posting and resume, as well as the following focus areas, try to match the skills mentioned in the job posting with those on the resume. Identify any gaps in the applicant''s skills based on the job requirements. Additionally, assess if the applicant''s past experiences cover the required tasks and responsibilities, pinpointing areas where the experience falls short.',
    'Based on the insights you just shared, provide actionable advice based on the job posting and the applicant''s resume. Clearly identify the applicant''s strengths and shortcomings. Offer constructive suggestions for addressing identified skills and experience gaps. Additionally, recommend specific courses, certifications and resume optimization strategies to enhance the applicant''s chances.'
]

# For 3-prompt architecture
def focusAreas(jobPost_resume):

    return prompts[0] + "\n\n<Job Post>" + jobPost_resume[0] + "\n<Job Post/> " + "\n\n<Resume>" + jobPost_resume[1] + "\n<Resume/>"

def idGaps3(areas):

    return prompts[1] + "\n\n<Areas>" + areas[0] + "\n<Areas/>"

def actAdv3():

    return prompts[2]
