from fastapi import FastAPI
 

app=FastAPI()

@app.get("/")
def title():
    return {"message": "Patent Management system API"}

@app.get("/about")
def about():
    return {"message": "A fully functional api to manage patents and their detalis"}




