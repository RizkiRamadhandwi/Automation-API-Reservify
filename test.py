import requests

auth_token = None
host = "localhost:8080"
version = "api/v1"


# login
def test_login_user_valid():
    global auth_token

    url = f"http://{host}/{version}/auth/login"
    expected_status = 200
    expected_message = {"message" : "Ok"}
    json_body = {
        "username": "admin",
        "password": "admin123"
    }

    response = requests.post(url, json=json_body)

    assert response.status_code == expected_status
    assert response.json().get("status", {})["message"] == expected_message["message"]

    auth_token = response.json().get("data", {}).get("token")

def test_login_user_invalid():
    url = f"http://{host}/{version}/auth/login"
    expected_status = 400
    expected_message = {"message" : "username atau password salah"}
    json_body = {
        "username": "admi",
        "password": "admin123"
    }

    response = requests.post(url, json=json_body)

    assert response.status_code == expected_status
    assert response.json()["message"] == expected_message["message"]

def test_login_user_invalid_username_nil():
    url = f"http://{host}/{version}/auth/login"
    expected_status = 400
    expected_message = {"message" : "username harus diisi"}
    json_body = {
        "password": "admin123"
    }

    response = requests.post(url, json=json_body)

    assert response.status_code == expected_status
    assert response.json()["message"] == expected_message["message"]

def test_login_user_invalid_password_nil():
    url = f"http://{host}/{version}/auth/login"
    expected_status = 400
    expected_message = {"message" : "password harus diisi"}
    json_body = {
        "username": "admin",
    }

    response = requests.post(url, json=json_body)

    assert response.status_code == expected_status
    assert response.json()["message"] == expected_message["message"]

def test_login_user_invalid_username_and_password_nil():
    url = f"http://{host}/{version}/auth/login"
    expected_status = 400
    expected_message = {"message" : "username dan password harus diisi"}
    json_body = {}

    response = requests.post(url, json=json_body)

    assert response.status_code == expected_status
    assert response.json()["message"] == expected_message["message"]


# EMPLOYEE
# list
def test_list_employees_valid():
    global auth_token
    assert auth_token is not None

    url = f"http://{host}/{version}/employees"
    expected_status = 200
    expected_message = {"message" : "Ok"}
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = requests.get(url, headers=headers)

    assert response.status_code == expected_status
    assert response.json().get("status", {})["message"] == expected_message["message"]

def test_list_employees_invalid_unauthorized():
    url = f"http://{host}/{version}/employees"
    expected_status = 401

    response = requests.get(url)

    assert response.status_code == expected_status


# findbyid
def test_find_by_id_employees_valid():
    global auth_token
    assert auth_token is not None

    url = f"http://{host}/{version}/employees/04395a49-4324-4b03-be6c-1b9eaf87ff09"
    expected_status = 200
    expected_message = {"message" : "Ok"}
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = requests.get(url, headers=headers)

    assert response.status_code == expected_status
    assert response.json().get("status", {})["message"] == expected_message["message"]

def test_find_by_id_employees_invalid_unauthorized():
    url = f"http://{host}/{version}/employees/04395a49-4324-4b03-be6c-1b9eaf87ff09"
    expected_status = 401

    response = requests.get(url)

    assert response.status_code == expected_status

def test_find_by_id_employees_invalid_id():
    global auth_token
    assert auth_token is not None

    url = f"http://{host}/{version}/employees/04"
    expected_status = 404
    expected_message = {"message" : "Employee with ID 04 not found"}
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = requests.get(url, headers=headers)

    assert response.status_code == expected_status
    assert response.json()["message"] == expected_message["message"]


#  findbyusername
def test_find_by_username_employees_valid():
    global auth_token
    assert auth_token is not None

    url = f"http://{host}/{version}/employees/username/Messi"
    expected_status = 200
    expected_message = {"message" : "Ok"}
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = requests.get(url, headers=headers)

    assert response.status_code == expected_status
    assert response.json().get("status", {})["message"] == expected_message["message"]

def test_find_by_username_employees_invalid_unauthorized():
    url = f"http://{host}/{version}/employees/username/Messi"
    expected_status = 401

    response = requests.get(url)

    assert response.status_code == expected_status

def test_find_by_username_employees_invalid_username():
    global auth_token
    assert auth_token is not None

    url = f"http://{host}/{version}/employees/username/m"
    expected_status = 404
    expected_message = {"message" : "Employee with Username m not found"}
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = requests.get(url, headers=headers)

    assert response.status_code == expected_status
    assert response.json()["message"] == expected_message["message"]


# create
# def test_create_employees_valid():
#     global auth_token
#     assert auth_token is not None

#     url = f"http://{host}/{version}/employees"
#     expected_status = 201
#     expected_message = {"message" : "Created"}
#     headers = {"Authorization": f"Bearer {auth_token}"}
#     json_body = {
#         "name": "Mbappe",
#         "username": "mbappe",
#         "password": "psg",
#         "role": "employee",
#         "division": "Striker",
#         "position": "Staff",
#         "contact": "0836124324"
#     }

#     response = requests.post(url, headers=headers, json=json_body)

#     assert response.status_code == expected_status
#     assert response.json().get("status", {})["message"] == expected_message["message"]

def test_create_employees_invalid_unauthorized():
    url = f"http://{host}/{version}/employees"
    expected_status = 401

    response = requests.post(url)

    assert response.status_code == expected_status

def test_create_employees_invalid_field():
    global auth_token
    assert auth_token is not None

    url = f"http://{host}/{version}/employees"
    expected_status = 400
    expected_message = {"message" : "oops, field required"}
    headers = {"Authorization": f"Bearer {auth_token}"}
    json_body = {
        "name": "Mbappe",
        "username": "bappe",
        "password": "psgg",
        "role": "employee",
        "division": "Striker",
        "position": "",
        "contact": ""
    }

    response = requests.post(url, headers=headers, json=json_body)

    assert response.status_code == expected_status
    assert response.json()["message"] == expected_message["message"]


# edit
# def test_edit_employees_valid():
#     global auth_token
#     assert auth_token is not None

#     url = f"http://{host}/{version}/employees"
#     expected_status = 200
#     expected_message = {"message" : "Updated"}
#     headers = {"Authorization": f"Bearer {auth_token}"}
#     json_body = {
#         "id": "ee90bc01-a267-4fc0-a6fd-885d1e18daf7",
#         "name": "M. Salah",
#         "username": "salah",
#         "password": "liverpool",
#         "role": "admin",
#         "division": "Striker",
#         "position": "Staff",
#         "contact": "0836124324"
#     }

#     response = requests.put(url, headers=headers, json=json_body)

#     assert response.status_code == expected_status
#     assert response.json().get("status", {})["message"] == expected_message["message"]

def test_edit_employees_invalid_unauthorized():
    url = f"http://{host}/{version}/employees"
    expected_status = 401

    response = requests.put(url)

    assert response.status_code == expected_status

def test_edit_employees_invalid_field():
    global auth_token
    assert auth_token is not None

    url = f"http://{host}/{version}/employees"
    expected_status = 400
    expected_message = {"message" : "oops, field required"}
    headers = {"Authorization": f"Bearer {auth_token}"}
    json_body = {
        "id": "ee90bc01-a267-4fc0-a6fd-885d1e18daf7",
        "name": "Mbappe",
        "username": "bappe",
        "password": "psgg",
        "role": "employee",
        "division": "Striker",
        "position": "",
        "contact": ""
    }

    response = requests.put(url, headers=headers, json=json_body)

    assert response.status_code == expected_status
    assert response.json()["message"] == expected_message["message"]




# FACILITIES
# list
def test_list_facilities_valid():
    global auth_token
    assert auth_token is not None

    url = f"http://{host}/{version}/facilities"
    expected_status = 200
    expected_message = {"message" : "Ok"}
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = requests.get(url, headers=headers)

    assert response.status_code == expected_status
    assert response.json().get("status", {})["message"] == expected_message["message"]

def test_list_facilities_invalid_unauthorized():
    url = f"http://{host}/{version}/facilities"
    expected_status = 401

    response = requests.get(url)

    assert response.status_code == expected_status


# findbyid
def test_find_by_id_facilities_valid():
    global auth_token
    assert auth_token is not None

    url = f"http://{host}/{version}/facilities/44aee759-8651-480d-9a9d-ee0c7867ebdc"
    expected_status = 200
    expected_message = {"message" : "Ok"}
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = requests.get(url, headers=headers)

    assert response.status_code == expected_status
    assert response.json().get("status", {})["message"] == expected_message["message"]

def test_find_by_id_facilities_invalid_unauthorized():
    url = f"http://{host}/{version}/facilities/44aee759-8651-480d-9a9d-ee0c7867ebdc"
    expected_status = 401

    response = requests.get(url)

    assert response.status_code == expected_status

def test_find_by_id_facilities_invalid_id():
    global auth_token
    assert auth_token is not None

    url = f"http://{host}/{version}/facilities/04"
    expected_status = 404
    expected_message = {"message" : "Facilities with ID 04 not found"}
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = requests.get(url, headers=headers)

    assert response.status_code == expected_status
    assert response.json()["message"] == expected_message["message"]


# create
# def test_create_facilities_valid():
#     global auth_token
#     assert auth_token is not None

#     url = f"http://{host}/{version}/facilities"
#     expected_status = 201
#     expected_message = {"message" : "Created"}
#     headers = {"Authorization": f"Bearer {auth_token}"}
#     json_body = {
#         "name": "Proyektor",
#         "quantity": 10
#     }

#     response = requests.post(url, headers=headers, json=json_body)

#     assert response.status_code == expected_status
#     assert response.json().get("status", {})["message"] == expected_message["message"]

def test_create_facilities_invalid_unauthorized():
    url = f"http://{host}/{version}/facilities"
    expected_status = 401

    response = requests.post(url)

    assert response.status_code == expected_status

def test_create_facilities_invalid_field():
    global auth_token
    assert auth_token is not None

    url = f"http://{host}/{version}/facilities"
    expected_status = 400
    expected_message = {"message" : "oops, field required"}
    headers = {"Authorization": f"Bearer {auth_token}"}
    json_body = {
        "name": "",
        "quantity": 10
    }

    response = requests.post(url, headers=headers, json=json_body)

    assert response.status_code == expected_status
    assert response.json()["message"] == expected_message["message"]


# edit
# def test_edit_facilities_valid():
#     global auth_token
#     assert auth_token is not None

#     url = f"http://{host}/{version}/facilities"
#     expected_status = 200
#     expected_message = {"message" : "Updated"}
#     headers = {"Authorization": f"Bearer {auth_token}"}
#     json_body = {
#         "id": "44aee759-8651-480d-9a9d-ee0c7867ebdc",
#         "name": "Printer",
#         "quantity": 10
#     }

#     response = requests.put(url, headers=headers, json=json_body)

#     assert response.status_code == expected_status
#     assert response.json().get("status", {})["message"] == expected_message["message"]

def test_edit_facilities_invalid_unauthorized():
    url = f"http://{host}/{version}/facilities"
    expected_status = 401

    response = requests.put(url)

    assert response.status_code == expected_status

def test_edit_facilities_invalid_field():
    global auth_token
    assert auth_token is not None

    url = f"http://{host}/{version}/facilities"
    expected_status = 400
    expected_message = {"message" : "oops, field required"}
    headers = {"Authorization": f"Bearer {auth_token}"}
    json_body = {
        "id": "44aee759-8651-480d-9a9d-ee0c7867ebdc",
        "name": "",
        "quantity": 10
    }

    response = requests.put(url, headers=headers, json=json_body)

    assert response.status_code == expected_status
    assert response.json()["message"] == expected_message["message"]


# ROOMS
# list
def test_list_rooms_valid():
    global auth_token
    assert auth_token is not None

    url = f"http://{host}/{version}/rooms"
    expected_status = 200
    expected_message = {"message" : "Ok"}
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = requests.get(url, headers=headers)

    assert response.status_code == expected_status
    assert response.json().get("status", {})["message"] == expected_message["message"]

def test_list_rooms_invalid_unauthorized():
    url = f"http://{host}/{version}/rooms"
    expected_status = 401

    response = requests.get(url)

    assert response.status_code == expected_status


# findbyid
def test_find_by_id_rooms_valid():
    global auth_token
    assert auth_token is not None

    url = f"http://{host}/{version}/rooms/5fee7bc3-f5f2-4186-be8b-db1354f1c754"
    expected_status = 200
    expected_message = {"message" : "Ok"}
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = requests.get(url, headers=headers)

    assert response.status_code == expected_status
    assert response.json().get("status", {})["message"] == expected_message["message"]

def test_find_by_id_rooms_invalid_unauthorized():
    url = f"http://{host}/{version}/rooms/5fee7bc3-f5f2-4186-be8b-db1354f1c754"
    expected_status = 401

    response = requests.get(url)

    assert response.status_code == expected_status

def test_find_by_id_rooms_invalid_id():
    global auth_token
    assert auth_token is not None

    url = f"http://{host}/{version}/rooms/04"
    expected_status = 404
    expected_message = {"message" : "Room with ID 04 not found"}
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = requests.get(url, headers=headers)

    assert response.status_code == expected_status
    assert response.json()["message"] == expected_message["message"]


# create
# def test_create_rooms_valid():
#     global auth_token
#     assert auth_token is not None

#     url = f"http://{host}/{version}/rooms"
#     expected_status = 201
#     expected_message = {"message" : "Created"}
#     headers = {"Authorization": f"Bearer {auth_token}"}
#     json_body = {
#         "name": "Ruang Jambu",
        # "room_type": "Meeting Room",
        # "capacity": 27,
        # "status": "available"
#     }

#     response = requests.post(url, headers=headers, json=json_body)

#     assert response.status_code == expected_status
#     assert response.json().get("status", {})["message"] == expected_message["message"]

def test_create_rooms_invalid_unauthorized():
    url = f"http://{host}/{version}/rooms"
    expected_status = 401

    response = requests.post(url)

    assert response.status_code == expected_status

def test_create_rooms_invalid_field():
    global auth_token
    assert auth_token is not None

    url = f"http://{host}/{version}/rooms"
    expected_status = 400
    expected_message = {"message" : "oops, field required"}
    headers = {"Authorization": f"Bearer {auth_token}"}
    json_body = {
        "name": "Ruang Adidharma",
        "room_type": "",
        "capacity": 27,
        "status": "available"
    }

    response = requests.post(url, headers=headers, json=json_body)

    assert response.status_code == expected_status
    assert response.json()["message"] == expected_message["message"]


# edit detail
# def test_edit_detail_rooms_valid():
#     global auth_token
#     assert auth_token is not None

#     url = f"http://{host}/{version}/rooms"
#     expected_status = 200
#     expected_message = {"message" : "Updated"}
#     headers = {"Authorization": f"Bearer {auth_token}"}
#     json_body = {
#         "id": "5fee7bc3-f5f2-4186-be8b-db1354f1c754",
#         "name": "Ruang Mangga",
        # "room_type": "Meeting Room",
        # "capacity": 27,
        # "status": "available"
#     }

#     response = requests.put(url, headers=headers, json=json_body)

#     assert response.status_code == expected_status
#     assert response.json().get("status", {})["message"] == expected_message["message"]

def test_edit_detail_rooms_invalid_unauthorized():
    url = f"http://{host}/{version}/rooms"
    expected_status = 401

    response = requests.put(url)

    assert response.status_code == expected_status

def test_edit_detail_rooms_invalid_field():
    global auth_token
    assert auth_token is not None

    url = f"http://{host}/{version}/rooms"
    expected_status = 400
    expected_message = {"message" : "oops, field required"}
    headers = {"Authorization": f"Bearer {auth_token}"}
    json_body = {
        "id": "5fee7bc3-f5f2-4186-be8b-db1354f1c754",
        "name": "",
        "room_type": "Meeting Room",
        "capacity": 27,
        "status": "available"
    }

    response = requests.put(url, headers=headers, json=json_body)

    assert response.status_code == expected_status
    assert response.json()["message"] == expected_message["message"]



# edit status
# def test_edit_status_rooms_valid():
#     global auth_token
#     assert auth_token is not None

#     url = f"http://{host}/{version}/rooms/status"
#     expected_status = 200
#     expected_message = {"message" : "Updated"}
#     headers = {"Authorization": f"Bearer {auth_token}"}
#     json_body = {
#         "id": "5fee7bc3-f5f2-4186-be8b-db1354f1c754",
#         "status": "unavailable"
#     }

#     response = requests.put(url, headers=headers, json=json_body)

#     assert response.status_code == expected_status
#     assert response.json().get("status", {})["message"] == expected_message["message"]

def test_edit_status_rooms_invalid_unauthorized():
    url = f"http://{host}/{version}/rooms"
    expected_status = 401

    response = requests.put(url)

    assert response.status_code == expected_status

def test_edit_status_rooms_invalid_field():
    global auth_token
    assert auth_token is not None

    url = f"http://{host}/{version}/rooms"
    expected_status = 400
    expected_message = {"message" : "oops, field required"}
    headers = {"Authorization": f"Bearer {auth_token}"}
    json_body = {
        "id": "5fee7bc3-f5f2-4186-be8b-db1354f1c754", 
        "status": ""
    }

    response = requests.put(url, headers=headers, json=json_body)

    assert response.status_code == expected_status
    assert response.json()["message"] == expected_message["message"]



# Room Facility

# list
def test_list_roomfacilities_valid():
    global auth_token
    assert auth_token is not None

    url = f"http://{host}/{version}/roomfacilities"
    expected_status = 200
    expected_message = {"message" : "Ok"}
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = requests.get(url, headers=headers)

    assert response.status_code == expected_status
    assert response.json().get("status", {})["message"] == expected_message["message"]

def test_list_roomfacilities_invalid_unauthorized():
    url = f"http://{host}/{version}/roomfacilities"
    expected_status = 401

    response = requests.get(url)

    assert response.status_code == expected_status


# findbyid
def test_find_by_id_roomfacilities_valid():
    global auth_token
    assert auth_token is not None

    url = f"http://{host}/{version}/roomfacilities/4d749751-77c2-491f-be17-a0cdc17f15a3"
    expected_status = 200
    expected_message = {"message" : "Ok"}
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = requests.get(url, headers=headers)

    assert response.status_code == expected_status
    assert response.json().get("status", {})["message"] == expected_message["message"]

def test_find_by_id_roomfacilities_invalid_unauthorized():
    url = f"http://{host}/{version}/roomfacilities/4d749751-77c2-491f-be17-a0cdc17f15a3"
    expected_status = 401

    response = requests.get(url)

    assert response.status_code == expected_status

def test_find_by_id_roomfacilities_invalid_id():
    global auth_token
    assert auth_token is not None

    url = f"http://{host}/{version}/roomfacilities/04"
    expected_status = 404
    expected_message = {"message" : "Roomfacilities with ID 04 not found"}
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = requests.get(url, headers=headers)

    assert response.status_code == expected_status
    assert response.json()["message"] == expected_message["message"]


# create
# def test_create_roomfacilities_valid():
#     global auth_token
#     assert auth_token is not None

#     url = f"http://{host}/{version}/roomfacilities"
#     expected_status = 201
#     expected_message = {"message" : "Created"}
#     headers = {"Authorization": f"Bearer {auth_token}"}
#     json_body = {
#         "roomId": "5fee7bc3-f5f2-4186-be8b-db1354f1c754",
        # "facilityId": "44aee759-8651-480d-9a9d-ee0c7867ebdc",
        # "quantity": 5,
        # "description": "add a new facility"
#     }

#     response = requests.post(url, headers=headers, json=json_body)

#     assert response.status_code == expected_status
#     assert response.json().get("status", {})["message"] == expected_message["message"]

def test_create_roomfacilities_invalid_unauthorized():
    url = f"http://{host}/{version}/roomfacilities"
    expected_status = 401

    response = requests.post(url)

    assert response.status_code == expected_status

def test_create_roomfacilities_invalid_field():
    global auth_token
    assert auth_token is not None

    url = f"http://{host}/{version}/roomfacilities"
    expected_status = 400
    expected_message = {"message" : "oops, field required"}
    headers = {"Authorization": f"Bearer {auth_token}"}
    json_body = {
        "roomId": "5fee7bc3-f5f2-4186-be8b-db1354f1c754",
        "facilityId": "",
        "quantity": 5,
        "description": "add a new facility"
    }

    response = requests.post(url, headers=headers, json=json_body)

    assert response.status_code == expected_status
    assert response.json()["message"] == expected_message["message"]


# edit
# def test_edit_roomfacilities_valid():
#     global auth_token
#     assert auth_token is not None

#     url = f"http://{host}/{version}/roomfacilities"
#     expected_status = 200
#     expected_message = {"message" : "Updated"}
#     headers = {"Authorization": f"Bearer {auth_token}"}
#     json_body = {
#         "id": "4d749751-77c2-491f-be17-a0cdc17f15a3",
#         "roomId": "5fee7bc3-f5f2-4186-be8b-db1354f1c754",
        # "facilityId": "44aee759-8651-480d-9a9d-ee0c7867ebdc",
        # "quantity": 5,
        # "description": "add a new facility"
#     }

#     response = requests.put(url, headers=headers, json=json_body)

#     assert response.status_code == expected_status
#     assert response.json().get("status", {})["message"] == expected_message["message"]

def test_edit_roomfacilities_invalid_unauthorized():
    url = f"http://{host}/{version}/roomfacilities"
    expected_status = 401

    response = requests.put(url)

    assert response.status_code == expected_status

def test_edit_roomfacilities_invalid_field():
    global auth_token
    assert auth_token is not None

    url = f"http://{host}/{version}/roomfacilities"
    expected_status = 400
    expected_message = {"message" : "oops, field required"}
    headers = {"Authorization": f"Bearer {auth_token}"}
    json_body = {
        "id": "4d749751-77c2-491f-be17-a0cdc17f15a3",
        "roomId": "5fee7bc3-f5f2-4186-be8b-db1354f1c754",
        "facilityId": "44aee759-8651-480d-9a9d-ee0c7867ebdc",
        "quantity": 0,
        "description": "add a new facility"
    }

    response = requests.put(url, headers=headers, json=json_body)

    assert response.status_code == expected_status
    assert response.json()["message"] == expected_message["message"]
