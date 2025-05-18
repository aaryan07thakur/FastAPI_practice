from fastapi import FastAPI
import json
 

app=FastAPI()


def load_json():
    with open("patent.json", "r") as f:
        data=json.load(f)
        return data


@app.get("/")
def title():
    return {"message": "Patent Management system API"}

@app.get("/about")
def about():
    return {"message": "A fully functional api to manage patents and their detalis"}


@app.get("/view")
def view():
    data=load_json()
    return data

