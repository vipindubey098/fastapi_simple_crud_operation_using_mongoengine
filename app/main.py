from fastapi import FastAPI, APIRouter, status, Path, Query, Body
# from models import Employee
from . import models
from mongoengine import connect
import json
from mongoengine.queryset.visitor import Q
from pydantic import BaseModel
from typing import Optional


app = FastAPI()
connect(db="crud", host="localhost", port=27017)




@app.get("/api/welcome")
def root():
    return {"message": "Welcome"}

@app.get("/get_all_employees")
def get_all_employees():
    employees = models.Employee.objects().to_json()
    employees_list = json.loads(employees)
    return{"employees": employees_list}

# Below only integers are allowed, but an integer can be negative value as well, now we have add validation, import path from fastapi
# put ... and add greater than 0
# three dot is basically specifying that this employee id should be required and it is not optional 

@app.get("/get_employee/{emp_id}")
def get_employee(emp_id: int = Path(...,gt=0)):
    # print(emp_id)
    employee = models.Employee.objects.get(emp_id=emp_id)
    #returning a dictionary
    employee_dict =  {
        "emp_id": employee.emp_id,
        "name": employee.name,
        "age": employee.age,
        "teams": employee.teams
    }

    return employee_dict

@app.get("/search_employees")
# mention this age is an integer, and specify that this can be none but whenever someone do provide this age it should be greater than 18. So this how we can achieve validation using query
def search_employees(name: str, age: int=Query(None, gt=18)):
    employees = json.loads(models.Employee.objects.filter(Q(name__icontains=name) | Q(age=age)).to_json())
    return{"employees":employees}

# serializer
class NewEmployee(BaseModel):
    emp_id: int
    name: str
    age: int = Body(None, gt=18)
    teams: list


@app.post("/add_employee")
def add_employee(employee: NewEmployee):
    new_employee = models.Employee(emp_id=employee.emp_id,
                                    name= employee.name,
                                    age = employee.age,
                                    teams = employee.teams
                                    )
    new_employee.save()
    return{"message":"Employee added successfully!"}

# serializer
class EmployeeUpdate(BaseModel):
    emp_id: int
    name: Optional[str]
    age: Optional[int]
    teams: Optional[list]

# @app.put("/employee")
# def update_employee(data: EmployeeUpdate):
#     # print(data)
#     data = dict(data)
#     # upd_employee = models.Employee.objects.update_one({'emp_id':data.emp_id},{"$set": data})
#     # upd_employee = models.Employee.objects(emp_id='...').update_one(data)
#     # upd_employee = models.Employee.objects().updatemany(emp_id=data['emp_id'],push_all=data)
#     # upd_employee = models.Employee.objects.update_one({'emp_id':data["emp_id"]}, {"$set": {"name":data["name"], "age":data["age"], "teams":data['teams']}})
#     prev = {'emp_id':data["emp_id"]}
#     next_ut = {"$set": {"name":data["name"], "age":data["age"], "teams":data['teams']}}
    
#     models.Employee.objects.update_one({"emp_id": data['emp_id']}, next_ut)

#     if upd_employee:
#         return {"message": f"Employee updated."}



@app.put("/employee")
def update_employee(data: EmployeeUpdate):
    # print(data)
    data = dict(data)
    
    models.Employee.objects(emp_id=data['emp_id']).update_one(**data)
    return {'status': "success"}



@app.delete("/deleteemployee/{emp_id}")
def delete_employee(emp_id):
    employee_obj = models.Employee.objects.get(emp_id=emp_id)
    employee_obj.delete()
    return {'status': "deletion successful"}