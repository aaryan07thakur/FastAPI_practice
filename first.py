from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
import json
import logging
from typing import Annotated,Literal


app=FastAPI()

class patient(BaseModel):
    name:Annotated[str, Field(..., description="The name of the patent")]
    patient_id:Annotated[str,Field(..., description="The ID of the patent", examples=['poo1'])]
    city:Annotated[str, Field(..., description="city where the patent is leaving")]
    age:Annotated[int,Field(..., gt=0, lt=120, description="age of the patent")]
    gender:Annotated[Literal['male','Female','other'], Field(..., description="Gender of the patend")]
    weight: Annotated[float, Field(..., gt=0, description="weight of the patent in Kg")]
    height:Annotated[float, Field(..., gt=0, description='height of the patent in cm')]

    @computed_field(return_type=float)
    @property
    def bmi(self):
        bmi=round(self.weight / ((self.height/100) ** 2), 2)
        return bmi
    
    @computed_field
    @property
    def vredict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"
        


def load_json():
    with open("patent.json", "r") as f:
        data=json.load(f)
        return data


def save_data(data):
        with open("patent.json", "w") as f:
            json.dump(data, f)



@app.get("/")
def title():
    return {"message": "Patent Management system API"}

@app.get("/about")
def about():
    return {"message": "A fully functional api to manage patients and their detalis"}


@app.get("/view")
def view():
    data=load_json()
    return data



@app.get("/patient/{patient_id}")
def view_patient(patient_id: str=Path(..., title="The ID of the patient to view", description="Enter the patent ID to view its details")):
    data = load_json()
    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(status_code=404, detail="patient not found")
    

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
   

@app.post("/create")
def create_patient(patient: patient):
    logging.info(f"creating new patent")
    #load existing data
    data=load_json()
    logging.info(f"data: {data}")

    #check if the patent is already present
    if patient.patient_id in data:
        raise HTTPException(status_code=400, detail="patent already exists")
    
    #add the new patent to the data
    logging.info(f"adding new patient {patient.patient_id}")
    data[patient.patient_id]=patient.dict()

    #save the data
    save_data(data)
    return JSONResponse(status_code=201, content={"message": "patent created Successfully", })

    
    # data[patent.patent_id]= patent.model_dump(exclude=['patent_id'])
    