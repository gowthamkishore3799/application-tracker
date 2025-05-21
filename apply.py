## First create a copy a folder,


import requests
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI
import logging
import uuid
import shutil
from datetime import datetime
from notion_client import Client
import sys

load_dotenv()




logging.basicConfig(filename = "output.log", format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Outputresponse(BaseModel):
    type: str
    text: str

class OutputList(BaseModel):
    responses: list[Outputresponse]



client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)
notion = Client(auth=os.environ.get("NOTION_API_KEY"))

def find_job_posting(job_posting):
    retrieved_content = {}
    for posting in job_posting:
        try:
            completion = client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful job assistant, helping me in extracting some metadata from job posting such as job_description, salary, location, job_title,company_name, job_qualifications, job_id, important_information(if any), project(ill be working if provided) \n\nif you find any other information, return the type as '''other'''. Dont exaggerate, just return the text provided from job posting. \n\nif the information is already extracted or processed, skip returning it and return the type as other. \nIf types is other, text can be returned as N/A.\nDont be returning same information twice, and return the type as other. \n\nRepeating once again\n1. Collect job_description, salary, location, job_title,company_name, job_qualifications, job_id, important_information(if any), project(ill be working if provided)  \n\n2. All these should be given as type and text should contain the information extracted\n\n3.If the information is already extracted, return the type as other and text as N/A. If you have retrieved all the content, dont extract just return the type as 'complete'. If the job contains prefered qualifications, append them all in job_qualifications, Make sure job_posting length is less than 2000 characters, if more than that, just phrase it accordingly."},
                    {"role": "assistant", "content": f"You have already collected this below information {retrieved_content}"},
                    {"role": "user", "content": str(posting)}
                ],
                response_format=OutputList,
            )
            response = completion.choices[0].message.parsed
            contents = response.responses

            for content in contents:
                if content.type != "other":
                    retrieved_content[content.type] = content.text
                
                if content.type == "complete":
                    logger.info(retrieved_content)
                    return retrieved_content
        except Exception as e:
            print(e)
    return retrieved_content;


def extract(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        for tag in soup.find_all(["aside", "footer", "nav", "style", "img", "time", "iframe", "input", "table"]):
            tag.decompose()
        job_posting={}
        job_posting = soup.find_all()

        job_posting = job_posting + [soup.title]
        content = find_job_posting(job_posting)
        return content
    except:
        logger.error("Error in Parsing job description")
    
    return ""

def integrateIntoNotion(posting):
    today = datetime.today()

    formatted_date = today.strftime('%Y-%m-%d')

    description = posting.get("job_description" , "")

    description = description[:2000] if len(description) > 2000 else description
    data_to_insert = {
    "parent": {
        "type": "database_id",
        "database_id": os.environ.get("DATABASE_ID")
    },
    "properties": {
        "Position": {
            "multi_select": [
                {
                    "name": posting["job_title"]
                }
            ]
        },
        "Company": {
            "title": [
                {
                    "text": {
                        "content": str(posting["company_name"])
                    }
                }
            ]
        },
        "Resume 1": {
            "url": posting["doc_url"]
        },
        "Compensation": {
            "rich_text": [
                {
                    "text": {
                        "content": str(posting.get("salary", "N/A"))
                    }
                }
            ]
        },
        "Qualification": {
            "rich_text": [
                {
                    "text": {
                        "content": str(posting.get("job_qualifications"), "N/A")
                    }
                }
            ]
        },
        "Location": {
            "rich_text": [
                {
                    "text": {
                        "content": str(posting["location"])
                    }
                }
            ]
        },
        "Job Description": {
            "rich_text": [
                {
                    "text": {
                        "content": str(description)
                    }
                }
            ]
        },
        "Stage": {
            "status": {
                "name": "Applied"
            }
        },
        "Apply date": {
            "date": {
                "start": formatted_date
            }
        },
        "Job URL": {
            "url": posting["url"]
        },
        "Job Id": {
            "rich_text": [
                {
                    "text": {
                        "content": posting.get("job_id", "N/A")
                    }
                }
            ]
        }
    }
}
    response = notion.pages.create(**data_to_insert)
def createApplication(posting):
    try:
        dirname = f"{os.environ.get("OUTPUT_DIR")}{posting.company}-{posting.job_title.replace(' ', '-').lower()}-{uuid.uuid4()}"
        os.mkdir(dirname)
    except:
        logger.error("Error in Creating Directory")

def apply(url, doc_url):
    posting = extract(url)
    posting["url"] = url;
    posting["doc_url"] = doc_url
    createApplication(posting)
    integrateIntoNotion(posting)


job_url = sys.argv[1]
doc_url = sys.argv[2]
apply(job_url, doc_url)
