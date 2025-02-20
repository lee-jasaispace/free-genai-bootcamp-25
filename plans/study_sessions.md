# Implementation Plan for /study_sessions POST Route

## Overview
This document provides a step-by-step guide for implementing the `/study_sessions` POST route in a Flask application. Each step is broken down into atomic tasks with checkboxes to track progress.

## Steps

### 1. **Define the Route**
- [x] Create a new function `create_study_session` inside `load(app)`
- [x] Use `@app.route('/api/study-sessions', methods=['POST'])` to define the endpoint
- [x] Use `@cross_origin()` to allow CORS support

### 2. **Validate the Request Data**
- [x] Extract the request JSON using `request.get_json()`
- [x] Check if required fields `group_id` and `study_activity_id` are present
- [x] Return a `400 Bad Request` error if any field is missing

### 3. **Insert Data into the Database**
- [x] Open a database cursor
- [x] Insert a new study session into `study_sessions` table with `group_id`, `study_activity_id`, and `created_at` timestamp
- [x] Retrieve the `id` of the newly created session
- [x] Commit the transaction

### 4. **Return a Response**
- [x] Construct a JSON response including the `id`, `group_id`, `study_activity_id`, and `created_at`
- [x] Return a `201 Created` response

### 5. **Handle Errors**
- [x] Wrap the logic in a `try-except` block
- [x] Return a `500 Internal Server Error` in case of database or server issues

## Implementation Code

```python
from flask import request, jsonify
from flask_cors import cross_origin
from datetime import datetime

def load(app):
    @app.route('/api/study-sessions', methods=['POST'])
    @cross_origin()
    def create_study_session():
        try:
            data = request.get_json()
            
            # Validate request data
            if not data or 'group_id' not in data or 'study_activity_id' not in data:
                return jsonify({"error": "Missing required fields: group_id, study_activity_id"}), 400
            
            group_id = data['group_id']
            study_activity_id = data['study_activity_id']
            created_at = datetime.utcnow()
            
            cursor = app.db.cursor()
            cursor.execute('''
                INSERT INTO study_sessions (group_id, study_activity_id, created_at)
                VALUES (?, ?, ?)
            ''', (group_id, study_activity_id, created_at))
            
            session_id = cursor.lastrowid
            app.db.commit()
            
            return jsonify({
                "id": session_id,
                "group_id": group_id,
                "study_activity_id": study_activity_id,
                "created_at": created_at
            }), 201
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
```

## Testing the Endpoint

### **1. Test with Valid Data**
#### **cURL Command:**
```sh
curl -X POST "http://localhost:5000/api/study-sessions" \
     -H "Content-Type: application/json" \
     -d '{"group_id": 1, "study_activity_id": 2}'
```
#### **Expected Response:**
```json
{
  "id": 123,
  "group_id": 1,
  "study_activity_id": 2,
  "created_at": "2025-02-20T12:00:00"
}
```

### **2. Test with Missing Fields**
#### **cURL Command:**
```sh
curl -X POST "http://localhost:5000/api/study-sessions" \
     -H "Content-Type: application/json" \
     -d '{}'
```
#### **Expected Response:**
```json
{
  "error": "Missing required fields: group_id, study_activity_id"
}
```

### **3. Test Error Handling**
#### **Simulating Database Failure:**
- [ ] Stop the database service before sending a request.
- [ ] Send a valid POST request to the endpoint.
- [ ] Ensure the response includes a `500 Internal Server Error`.

#### **cURL Command:**
```sh
curl -X POST "http://localhost:5000/api/study-sessions" \
     -H "Content-Type: application/json" \
     -d '{"group_id": 1, "study_activity_id": 2}'
```
#### **Expected Response:**
```json
{
  "error": "(Database error message)"
}
```

## Next Steps
- [ ] Implement additional validation, such as checking if `group_id` and `study_activity_id` exist in the database.
- [ ] Add logging for better debugging.
- [ ] Write unit tests using `pytest` or `unittest`.

---
This plan ensures a structured approach to implementing the `/study_sessions` POST route while maintaining clarity, robustness, and ease of testing.

