from fastapi import FastAPI, Path, HTTPException, Query
import json
import logging
 

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
    

@app.get("/sort")
def sort_patent(sort_by:str=Query(..., description="sort on the basis of weight and height"),
                order:str=Query("asc",description="sort in ascending or descending order")):
    logging.info(f"sort_by: {sort_by}")
    
    valid_fields=["weight", "height"]
    logging.info(f"sort_by: {sort_by}")
    if sort_by not in valid_fields:
        logging.error(f"invalid field")
        raise HTTPException(status_code=400, detail=f"Invalid  fields select from {valid_fields}")
    
    if not  order in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="invalid order, select between asc and desc")
    
    logging.info(f"order: {order}")
    data=load_json()
    sort_order=True if order=="asc" else False
    sorted_data=sorted(data.values(), key=lambda x:x.get(sort_by,0), reverse=sort_order)

    return sorted_data
   
