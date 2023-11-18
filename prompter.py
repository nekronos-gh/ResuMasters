## Different prompts to be fed into Llama to generate the comparisons
prompts = [
    'Analyze the following job posting and attached resume. Identify key skills mentioned in the job posting, compare the applicant''s job history with the job requirements, and assess to what extent the applicant''s education aligns with the position. Provide insights into how relevant relevant the applicant''s experiences and qualifications are.',
    'Given the mentioned job posting and resume, as well as the following focus areas, try to match the skills mentioned in the job posting with those on the resume. Identify any gaps in the applicant''s skills based on the job requirements. Additionally, assess if the applicant''s past experiences cover the required tasks and responsibilities, pinpointing areas where the experience falls short.',
    'Based on the insights you just shared, provide actionable advice based on the job posting and the applicant''s resume. Clearly identify the applicant''s strengths and shortcomings. Offer constructive suggestions for addressing identified skills and experience gaps. Additionally, recommend specific courses, certifications and resume optimization strategies to enhance the applicant''s chances.',
    'You are now an expert career counselor. Given the applicant''s resume, as well as the job description, execute these 2 steps: 1) {Summarize the applicant''s main strengths and relevant experience} 2) {Write a cover letter for this job opening that strongly conveys the applicant''s skills, passions, and fit for the job. Make sure it is a memorable letter that will catch the recruiter''s eye.',
    'We are analyzing a job applicant''s resume, as well as the description of their target job. You have decades of experience working in this job''s industry. Based on the applicant''s resume, as well as the job description, {identify the applicant''s main relevant experience, as well as their shortcomings}. Additionally, {propose a project that the applicant could add to their portfolio. The project should be relevant to the job opening and should showcase the applicant''s skills and experience. Make sure to include a brief description of the project, as well as the skills and experience it will demonstrate.}',
    'You are an expert career counselor, tasked with analyzing the following job posting and attached resume. Let''s work step by step. You will 1) {Identify key skills mentioned in the job posting}, 2) {compare the applicant''s qualifications with the job requirements}, and 3) {say TRUE if the applicant''s qualifications align with the job description, and FALSE  otherwise}'
]

# For 3-prompt architecture
def focusAreas(jobPost_resume):
    return prompts[0] + "\n\n<Job Post>" + jobPost_resume[0] + "\n<Job Post/> " + "\n\n<Resume>" + jobPost_resume[1] + "\n<Resume/>"

def idGaps3(areas):
    return prompts[1] + "\n\n<Areas>" + areas[0] + "\n<Areas/>"

def actAdv3():
    return prompts[2]

# For cover letters. The UI should incite users to use this functionality after skills & gaps identification
def coverLetter(jobPost_resume):
    return prompts[3] + "\n\n<Job Post>" + jobPost_resume[0] + "\n<Job Post/> " + "\n\n<Resume>" + jobPost_resume[1] + "\n<Resume/>"

# For the proposal of projects for the applicant's portfolio
def proposeProject(jobPost_resume):
    return prompts[4] + "\n\n<Job Post>" + jobPost_resume[0] + "\n<Job Post/> " + "\n\n<Resume>" + jobPost_resume[1] + "\n<Resume/>"

# To identify if a candidate should apply to a job
def match(jobPost_resume):
    return prompts[5] + "\n\n<Job Post>" + jobPost_resume[0] + "\n<Job Post/> " + "\n\n<Resume>" + jobPost_resume[1] + "\n<Resume/>"