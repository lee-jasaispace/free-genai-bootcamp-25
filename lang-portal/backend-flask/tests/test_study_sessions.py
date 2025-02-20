import pytest
from datetime import datetime
from unittest.mock import MagicMock

def test_create_study_session_success(client, app):
    # Test data
    test_data = {
        "group_id": 1,
        "study_activity_id": 2
    }
    
    # Make the request
    response = client.post('/api/study-sessions', json=test_data)
    
    # Print error message if status code is not 201
    if response.status_code != 201:
        print("\nError response:", response.get_json())
    
    # Assert response status code
    assert response.status_code == 201
    
    # Assert response structure
    data = response.get_json()
    assert 'session' in data
    session = data['session']
    
    # Assert all required fields are present
    assert 'id' in session
    assert 'group_id' in session
    assert 'activity_id' in session
    assert 'start_time' in session
    assert 'end_time' in session
    assert 'review_items_count' in session
    
    # Assert field values
    assert session['group_id'] == test_data['group_id']
    assert session['activity_id'] == test_data['study_activity_id']
    assert session['review_items_count'] == 0
    assert session['end_time'] == session['start_time']

def test_create_study_session_missing_fields(client):
    # Test with empty data
    response = client.post('/api/study-sessions', json={})
    assert response.status_code == 400
    assert "Missing required fields" in response.get_json()['error']
    
    # Test with partial data
    response = client.post('/api/study-sessions', json={"group_id": 1})
    assert response.status_code == 400
    assert "Missing required fields" in response.get_json()['error']

def test_create_study_session_database_error(client, app, mocker):
    # Mock database cursor to raise an exception
    mock_cursor = MagicMock()
    mock_cursor.execute.side_effect = Exception("Database error")
    
    # Mock app.db.cursor to return our mock
    mocker.patch.object(app.db, 'cursor', return_value=mock_cursor)
    
    # Test data
    test_data = {
        "group_id": 1,
        "study_activity_id": 2
    }
    
    # Make request and verify error response
    response = client.post('/api/study-sessions', json=test_data)
    assert response.status_code == 500
    assert "error" in response.get_json() 