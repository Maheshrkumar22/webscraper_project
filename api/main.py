from typing import Union
#from requests_html import AsyncHTMLSession
from url_scrape_data import scrape_data
import json
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

def process(url_name):

    results_json_string = scrape_data(url_name)
    # Parse the JSON string back into a Python list/dictionary
    results_list = json.loads(results_json_string)
    return results_list
    


@app.get("/url/{url_name:path}")
def read_item(url_name: str, q: Union[str, None] = None):
    results_json = process(url_name)
    return results_json