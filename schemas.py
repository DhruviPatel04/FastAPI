
def individual_serial_student(student) -> dict:
    return{
        "name": student["name"],
        "dob": student["dob"],
        "email": student["email"],
        "course": student["course"]
        
    }

def list_serial_student(Student_info) -> list:
    return[individual_serial_student(student) for student in Student_info]





def serialize_user(user) -> dict:
    return {
        "username": user["username"],
        "password": user["password"]
    }

def serialize_users(users) -> list:
    return [serialize_user(user) for user in users]

def individual_serial_module(module) -> dict:
    return{
        "name": module["name"],
        "description": module["description"],
        "credits": module["credits"],
        "department_id": str(module["department_id"])
    }




def list_serial_module(module_info) -> list:
    return[individual_serial_module(module) for module in module_info]



def individual_serial_material(material) -> dict:
    return{
        "title": material["title"],
        "description": material["description"],
        "file_URL": str(material["file_URL"]),
        "module_id": str(material["module_id"])
    }

def list_serial_material(material_info) -> list:
    return[individual_serial_material(material) for material in material_info]







def individual_serial_assessment(assessment) -> dict:
    return{
        "title": assessment["title"],
        "description": assessment["description"],
        "UploadFile": assessment["UploadFile"],
        "deadline": str(assessment["deadline"]),
        "status": assessment["status"],
        "module_id": str(assessment["module_id"])
    }

def list_serial_assessment(assessment_info) -> list:
    return[individual_serial_assessment(assessment) for assessment in assessment_info]




def individual_serial_feedback(feedback) -> dict:
    return{
        "student_id": str(feedback["student_id"]),
        "assessment_id": str(feedback["assessment_id"]),
        "grade": str(feedback["grade"]),
        "comments": str(feedback["comments"])
    }

def list_serial_feedback(feedback_info) -> list:
    return[individual_serial_feedback(feedback) for feedback in feedback_info]
    