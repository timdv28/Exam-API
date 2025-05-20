from fastapi import FastAPI
import csv

df = csv.reader(questions_en.xlsx)

api = FastAPI(
    title='My API'
)
@api.get('/')
def get_index():
    return {'data': 'hello world'}