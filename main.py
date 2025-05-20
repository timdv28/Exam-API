from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel
from typing import Optional
from fastapi import HTTPException
import random

questions = pd.read_excel('questions_en.xlsx')
identifiers = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine"
}

api = FastAPI(
    title='MCQ creation'
)

# class Login(BaseModel):
#     username: str
#     password: str

# class Ask(BaseModel):    
#     qnumber: int
#     type: Optional[str] = None
#     subject: Optional[str] = None

# Hello world
# @api.get('/')
# def get_index():
#     return {'data': 'hello world'}

possible_q_amount = [5,10,20]
# Get the number of questions

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

    for i in range(qnumber):
        choices = {}
        question = q['question'].iloc[i]
        
        choices['A'] = q['responseA'].iloc[i]
        choices['B'] = q['responseB'].iloc[i]
        # if q['responseC'].iloc[i]:
        #     choices['C'] = q['responseC'].iloc[i]
        # if q['responseD'].iloc[i]:
        #     choices['D'] = q['responseD'].iloc[i]
        
        Q[f'Question {i+1}'] = q['question'].iloc[i]
        
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
