# Part 1 - Create a Python Rest API endpoint
# Create a CRUD Rest API endpoint for Healthcare Provider directory. Use Python - FastAPI for building the Rest APIs.
# Store the data as an in-memory Dictionary.

# Part 2 - Persist the data in a file
# For the above use case, now serialise the objects and persist them in a file.

# Part 3 - Add Front end
# Build a Frontend for the application in simple HTML and CSS

# Invokation: hypercorn main:app --reload

import pickle
import uuid
from enum import Enum
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.responses import RedirectResponse

app = FastAPI()
db = {}

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


class status(int, Enum):
    active = 1
    inactive = 0


class Provider(BaseModel):
    active: Optional[status] = 1
    name: str = ""
    qualification: str = ""
    speciality: str = ""
    phone: str = ""
    department: Optional[str] = None
    organization: str = ""
    location: Optional[str] = None
    address: str = ""


@app.on_event("startup")
def on_startup():
    global db
    try:
        with open('database', 'rb') as database:
            db = pickle.load(database)
    except:
        pass


@app.on_event("shutdown")
def on_shutdown():
    global db
    with open('database', 'wb') as database:
        pickle.dump(db, database)


@app.get("/pages/{val}", response_class=HTMLResponse)
async def pages(request: Request, val: str):
    return templates.TemplateResponse(val, {
        "request": request,
        "data": db
    })


def get_uuid(param: str, value: str):
    if(param == 'active'):
        try:
            value = int(value)
        except:
            return []
    results = []
    for uuid in db:
        try:
            if(db[uuid][param] == value):
                results.append(uuid)
        except:
            return []
    return results


@app.get('/providers')
def get_providers():
    return [db[uuid] for uuid in db.keys()]


@app.get("/")
async def home():
    response = RedirectResponse(url='/pages/index.html')
    return response


@app.get('/get_provider/{field}={value}')
def get_provider(field: str, value: str):
    entries = get_uuid(field, value)
    results = [db[entry] for entry in entries]
    return (results if results else [])


@app.put('/create_provider')
def create_provider(provider: Provider):
    pro_uuid = str(uuid.uuid4())
    db[pro_uuid] = provider.dict()
    db[pro_uuid]['providerID'] = pro_uuid
    return db[pro_uuid]


@app.delete('/delete_provider/{field}={value}')
def delete_provider(field: str, value: str):
    entries = get_uuid(field, value)
    results = []
    for entry in entries:
        results.append(db[entry])
        del db[entry]
    return (results if results else [])


@ app.post('/update_provider/{id}')
def update_provider(id: str, active=None, name=None, qualification=None, speciality=None, phone=None, department=None, organization=None, location=None, address=None):
    if(id in db.keys()):
        try:
            if(active is not None):
                if(active == 'active'):
                    db[id]['active'] = status.active
                elif(active == 'inactive'):
                    db[id]['active'] = status.inactive
        except:
            return "Invalid Active Status!"

        db[id]['name'] = (
            name if name is not None else db[id]['name'])

        db[id]['qualification'] = (
            qualification if qualification is not None else db[id]['qualification'])

        db[id]['speciality'] = (
            speciality if speciality is not None else db[id]['speciality'])

        db[id]['phone'] = (
            phone if phone is not None else db[id]['phone'])

        db[id]['department'] = (
            department if department is not None else db[id]['department'])

        db[id]['organization'] = (
            organization if organization is not None else db[id]['organization'])

        db[id]['location'] = (
            location if location is not None else db[id]['location'])

        db[id]['address'] = (
            address if address is not None else db[id]['address'])
        return "SUCCESS!! Provider Details Updated."
    else:
        return "Provider not found!!"


@app.get("/fe/get_providers", response_class=HTMLResponse)
async def fe_get_providers(request: Request, field, value):
    results = get_provider(field, value)
    results_dict = {}
    for ele in results:
        results_dict[ele['providerID']] = ele
    return templates.TemplateResponse("provider.html", {
        "request": request,
        "data": results_dict
    })


@app.get("/fe/create_provider", response_class=HTMLResponse)
async def fe_create_providers(request: Request, name, active, qualification, speciality, phone,  organization, address, location=None, department=None):
    if(active == "active"):
        active = status.active
    else:
        active = status.inactive
    new_pro = Provider()
    new_pro.active = active
    new_pro.name = name
    new_pro.qualification = qualification
    new_pro.speciality = speciality
    new_pro.phone = phone
    new_pro.organization = organization
    new_pro.address = address
    new_pro.location = location
    new_pro.department = department
    create_provider(new_pro)
    return templates.TemplateResponse("create.html", {
        "request": request,
        "data": db,
        "message": "Provider Created Successfully!!"
    })


@app.get("/fe/update_provider", response_class=HTMLResponse)
async def fe_update_providers(request: Request, providerID, name, active, qualification, speciality, phone, department, organization, location, address):
    name = None if name == "" else name
    active = None if active == "" else active
    qualification = None if qualification == "" else qualification
    speciality = None if speciality == "" else speciality
    phone = None if phone == "" else phone
    organization = None if organization == "" else organization
    address = None if address == "" else address
    location = None if location == "" else location
    department = None if department == "" else department
    update_provider(providerID, active, name, qualification, speciality,
                    phone, department, organization, location, address)
    return templates.TemplateResponse("update.html", {
        "request": request,
        "data": db,
        "message": "Provider Updated Successfully!!"
    })


@app.get("/fe/delete_providers", response_class=HTMLResponse)
async def fe_delete_providers(request: Request, field, value, button):
    if(button == "preview"):
        results = get_provider(field, value)
        results_dict = {}
        for ele in results:
            results_dict[ele['providerID']] = ele
        return templates.TemplateResponse("delete.html", {
            "request": request,
            "data": results_dict,
        })
    results = get_uuid(field, value)
    for ele in results:
        del db[ele]
    return templates.TemplateResponse("delete.html", {
        "request": request,
        "data": db,
        "message": "Records Deleted Successfully!!"
    })
