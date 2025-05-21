from fastapi import FastAPI, Path, HTTPException
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



@app.get("/patient/{patent_id}")
def view_patient(patent_id: str=Path(..., title="The ID of the patent to view", description="Enter the patent ID to view its details")):
    data = load_json()
    if patent_id in data:
        return data[patent_id]
    else:
        raise HTTPException(status_code=404, detail="patent not found")