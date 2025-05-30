from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import json
import logging
import os
from typing import Annotated, Literal, Optional

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Pydantic Models
class Patient(BaseModel):
    """Model for patient details"""
    patient_id: Annotated[str, Field(..., description="The ID of the patient", examples=["p001"])]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description="City where the patient lives")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
    Gender: Annotated[Literal["male", "Female", "other"], Field(..., description="Gender of the patient")]
    weight: Annotated[float, Field(..., gt=0, description="Weight in kg")]
    height: Annotated[float, Field(..., gt=0, description="Height in feet")]




class PatientUpdate(BaseModel):
    """Model for updating patient details"""
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    Gender: Annotated[Optional[Literal["male", "Female"]], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


# Helper functions
JSON_FILE = "patent.json"

def load_json():
    """Load data from JSON file safely"""
    logging.info("Loading data from JSON file")
    if not os.path.exists(JSON_FILE):
        logging.warning("JSON file does not exist. Returning empty list.")
        return []

    try:
        with open(JSON_FILE, "r") as f:
            content = f.read()
            if not content.strip():  # Check if file is empty
                logging.warning("JSON file is empty. Returning empty list.")
                return []
            return json.loads(content)
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in file: {e}")
        return []


def save_data(data):
    """Save data to JSON file"""
    logging.info("Saving data to JSON file")
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)


# API Endpoints
@app.get("/")
def root():
    logging.info("Accessing the root endpoint")
    return {"message": "Patient Management System API"}


@app.get("/about")
def about():
    logging.info("Accessing the about endpoint")
    return {"message": "A fully functional API to manage patients and their details"}


@app.get("/view")
def view_patients():
    """View all patients or return empty list if no data"""
    logging.info("Accessing the view endpoint")
    data = load_json()
    if data:
        return JSONResponse(status_code=200, content={"message": "Patients found", "data": data})
    else:
        return JSONResponse(status_code=200, content={"message": "No patients found", "data": []})



@app.post("/create")
def create_patient(patient: Patient):
    """Create a new patient and save to JSON file"""
    logging.info("Accessing the create endpoint")


    data = load_json()
    logging.info(f"Current data: {data}")

    # Check if patient_id already exists
 
    if any(p["patient_id"] == patient.patient_id for p in data):
        raise HTTPException(status_code=400, detail="Patient ID already exists")
    logging.info(f"Patient ID {patient.patient_id} does not exist, proceeding to create new patient")

    # Convert pydantic model to dict and append
    data.append(patient.dict())
    logging.info(f"Adding new patient: {patient.dict()}")

    # Save back to file
    save_data(data)

    return JSONResponse(
        status_code=200,
        content={"message": "Patient created successfully", "data": patient.dict()}
    )

@app.get("/view/{patient_id}")
def view_patient(patient_id: str):
    """View a specific patient by ID"""
    data=load_json()
    logging.info(f"Accessing the view_patient endpoint for patient_id: {patient_id}")
    for patient in data:
        logging.info(f"checking patient: {patient_id}")
        if patient["patient_id"] == patient_id.lower():
            logging. info(f"patient found: {patient}")
            return JSONResponse(status_code=200, 
                                content={"message": "patient Found", "data":patient})
    raise HTTPException(status_code=404, detail="patient not found")




@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    logging.info(f"Accessing the update endpoint for patient_id: {patient_id}")
    """Update a specific patient by ID"""

    data = load_json()

    # Check if the patient exists
    found = False
    updated_patient = None

    for patient in data:
        if patient["patient_id"] == patient_id:
            found = True
            updated_patient = patient

            # Update only provided fields
            for field, value in patient_update.model_dump(exclude_unset=True).items():
                if value is not None:
                    patient[field] = value
            break

    if not found:
        logging.error(f'Patient with ID {patient_id} not found')
        raise HTTPException(status_code=404, detail="Patient not found")

    # Save the updated data
    save_data(data)

    logging.info(f"Updated patient: {updated_patient}")
    return JSONResponse(
        status_code=200,
        content={"message": "Patient updated successfully", "data": updated_patient}
    )



@app.delete("/delete/{patient_id}")
def delete_patient(patient_id:str):
    data=load_json()
    logging.info(data)
    for i, patient in enumerate(data):
        if patient["patient_id"] == patient_id:
            logging.info(f"Deleting patient with ID: {patient_id}")
            del data[i]
            save_data(data)
            return JSONResponse(status_code=200, content={"message": "Patient deleted successfully"})
    logging.error(f"Patient with ID {patient_id} not found")
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
    data = load_json()
    sorted_data = sorted(data, key=lambda x: x.get(sort_by, 0), reverse=(order == "desc"))
    logging.info(f"Sorted data: {sorted_data}")
    


    # logging.info(f"order: {order}")
    # data=load_json()
    # sort_order=True if order=="asc" else False
    # sorted_data=sorted(data.value(), key=lambda x:x.get(sort_by,0), reverse=sort_order)

    return sorted_data
   
