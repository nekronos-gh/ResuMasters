## Uses the functions from the prompter.py file to generate jsons for the LLM

import prompter

def getInputs():
    # Gets the inputs from the user
    jobPost = input("Enter the job post: ")
    resume = input("Enter the resume: ")
    return jobPost, resume

def toJSON(prompt, name):
    # Converts the prompt into a json file
    json = {"prompt": prompt}
    with open(name + ".json", "w") as file:
        json.dump(json, file)

    file.close()

def step(step, params):
    ## Get all the elements of list params, regardless of how many there are:
    prompt = step(params)
    toJSON(prompt, step.__name__)
    return input('Log response to ' + step.__name__ + 'from the LLM: ')


## Things to be executed:

def singlePrompt():
    jobPost, resume = getInputs()
    onePrompt = prompter.onePrompt(jobPost, resume)
    toJSON(onePrompt, "onePrompt")

def allSteps():
    jobPost, resume = getInputs()

    #Step 1
    reqs = step(prompter.xtractReqs, [jobPost])
    #Step 2
    info = step(prompter.xtractResume, [resume])
    #Step 3
    comp = step(prompter.compare, [reqs, info])
    #Step 4
    gaps = step(prompter.gaps, [comp])
    #Step 5
    advice = step(prompter.advice, [gaps])
    #Step 6
    ranked = step(prompter.priorities, [gaps, advice])
    #Step 7
    summary = prompter.summary([comp, gaps, ranked])
    toJSON(summary, "summary")