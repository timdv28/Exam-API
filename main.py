from fastapi import FastAPI
from fastapi import Header
from fastapi import HTTPException
import pandas as pd
import random
from pydantic import BaseModel
from typing import Optional


questions = pd.read_excel('questions_en.xlsx')
identifiers = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine"
}
possible_q_amount = [5,10,20]

api = FastAPI(
    title='MCQ creation'
)

class Login(BaseModel):
    username: str
    password: str

@api.put('/login')
def put_login(login: Login,username):
    # Check if the username is known
    try:
        logging_in = list(filter(lambda x: x.get(username) == str(username), 
                                 identifiers))[0]
    except:
        raise HTTPException(
            status_code=404,
            detail='Username not known')
        
    # Check if the password belongs to the username

    return {logging_in}

# Try to get the list of questions
@api.get('/Q/{qnumber:int}/type/{use}')
def get_questions(qnumber,use):
    Q = {} # Empty dictionary for the questions and the possible answers
    # Create a dataframe with all elligible questions
    
    q = questions.loc[questions['subject']==use]
    # q.sample(frac=1).reset_index(drop=True)
    
    # Confirm the number of questions
    if qnumber in possible_q_amount: 
        flag = True
    else:
        raise HTTPException(
            status_code=404,
            detail='Wrong amount of questions, choose 5, 10 or 20')
    
    # Check if we have enough questions to choose from
    # if qnumber <= q.size:
    #     flag = True
    # else:
    #     raise HTTPException(
    #         status_code=404,
    #         detail='Tried to pull more questions than there are available. Loosen requirements or reduce amount of questions')
    
    """Get a list of questions
    """
    li = list(range(qnumber))
    random.shuffle(li)
    j = 1
    for i in li:
        choices = {}
        question = str(q['question'].iloc[i])
        
        choices['A'] = q['responseA'].iloc[i]
        choices['B'] = q['responseB'].iloc[i]
        if q['responseC'].iloc[i]:
            choices['C'] = q['responseC'].iloc[i]
        # if q['responseD'].iloc[i]:
        #     choices['D'] = q['responseD'].iloc[i]
        
        Q[f'Question {j} -- '+question] = choices #q['question'].iloc[i]
        j += 1
    # q_list = questions.where(questions['subject'] == use) 
    return {'Quiz': Q,
            'Amount': qnumber}

# @api.post('/')
# def post_index():
#     return {
#         'method': 'post',
#         'endpoint': '/'
#         }



### Possible errors
# Fewer questions pulled than the amount of required questions
