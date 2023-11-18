import prompter
import json

## Uses the functions from the prompter.py file to generate jsons for the LLM

# write a function ro read a .txt file and return a string containing all lines
def readTxtFile(filename):
    file = open(filename, "r")
    text = file.read()
    file.close()
    return text

def getInputs():
    # Gets the inputs from the user
    input("Confirm that the job post is in jobPost.txt and the resume is in resume.txt. Press enter to continue: ")
    jobPost = readTxtFile("jobPost.txt")
    resume = readTxtFile("resume.txt")
    return jobPost, resume

def toJSON(prompt, name):
    # Converts the prompt into a json file
    print(prompt)
    full = {"instances": [{"prompt": prompt, "max_length": 200}]}
    with open('.\\jsons\\' + name + ".json", "w") as file:
        json.dump(full, file)

    file.close()

def step(step, params):
    ## Get all the elements of list params, regardless of how many there are:
    prompt = step(params)
    toJSON(prompt, step.__name__)
    input('Log response to ' + step.__name__ + ' from the LLM in response.txt. Press enter to continue: ')
    return readTxtFile("response.txt")


## Things to be executed:

def singlePrompt():
    jobPost, resume = getInputs()
    onePrompt = prompter.onePrompt([jobPost, resume])
    toJSON(onePrompt, "onePrompt")
    input('Log response from the LLM in ./responses/singlePrompt.txt. Press enter to end.')

def multiPrompt():
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
    ranked = step(prompter.prioritize, [gaps, advice])
    #Step 7
    summary = prompter.summarize([comp, gaps, ranked])
    toJSON(summary, "summary")
    input('Log final response from the LLM in ./responses/multiPrompt.txt. Press enter to end.')

multiPrompt()