import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

original_activities = {
    'Chess Club': {
        'description': 'Learn strategies and compete in chess tournaments',
        'schedule': 'Fridays, 3:30 PM - 5:00 PM',
        'max_participants': 12,
        'participants': ['michael@mergington.edu', 'daniel@mergington.edu']
    },
    'Programming Class': {
        'description': 'Learn programming fundamentals and build software projects',
        'schedule': 'Tuesdays and Thursdays, 3:30 PM - 4:30 PM',
        'max_participants': 20,
        'participants': ['emma@mergington.edu', 'sophia@mergington.edu']
    },
    'Gym Class': {
        'description': 'Physical education and sports activities',
        'schedule': 'Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM',
        'max_participants': 30,
        'participants': ['john@mergington.edu', 'olivia@mergington.edu']
    },
    'Basketball Team': {
        'description': 'Competitive basketball team and intramural games',
        'schedule': 'Mondays and Thursdays, 4:00 PM - 5:30 PM',
        'max_participants': 15,
        'participants': ['alex@mergington.edu']
    },
    'Soccer Club': {
        'description': 'Soccer practice and friendly matches',
        'schedule': 'Wednesdays and Saturdays, 3:30 PM - 5:00 PM',
        'max_participants': 22,
        'participants': ['ryan@mergington.edu', 'lucas@mergington.edu']
    },
    'Art Club': {
        'description': 'Painting, drawing, and sculpture techniques',
        'schedule': 'Tuesdays, 3:30 PM - 5:00 PM',
        'max_participants': 18,
        'participants': ['aisha@mergington.edu']
    },
    'Drama Club': {
        'description': 'Theater productions and acting workshops',
        'schedule': 'Wednesdays, 4:00 PM - 5:30 PM',
        'max_participants': 25,
        'participants': ['marcus@mergington.edu', 'lucy@mergington.edu']
    },
    'Debate Club': {
        'description': 'Public speaking and competitive debate',
        'schedule': 'Thursdays, 3:30 PM - 5:00 PM',
        'max_participants': 16,
        'participants': ['noah@mergington.edu']
    },
    'Science Olympiad': {
        'description': 'STEM competitions and hands-on science experiments',
        'schedule': 'Mondays and Fridays, 3:30 PM - 5:00 PM',
        'max_participants': 20,
        'participants': ['zoe@mergington.edu', 'ben@mergington.edu']
    }
}

@pytest.fixture(autouse=True)
def reset_activities():
    activities.clear()
    activities.update(original_activities)

class TestRootEndpoint:
    def test_root_redirect(self):
        # Arrange
        test_client = TestClient(app, follow_redirects=False)
        # Act
        response = test_client.get('/')
        # Assert
        assert response.status_code == 307
        assert response.headers['location'] == '/static/index.html'

class TestGetActivitiesEndpoint:
    def test_get_activities_returns_activity_dict(self):
        # Arrange
        # Act
        response = client.get('/activities')
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert 'Chess Club' in data
        assert 'Programming Class' in data

    def test_get_activities_fields_present(self):
        # Arrange
        # Act
        response = client.get('/activities')
        # Assert
        activity = response.json()['Chess Club']
        assert 'description' in activity
        assert 'schedule' in activity
        assert 'max_participants' in activity
        assert 'participants' in activity

class TestSignupEndpoint:
    def test_signup_success(self):
        # Arrange
        email = 'newstudent@mergington.edu'
        # Act
        response = client.post(f'/activities/Chess Club/signup?email={email}')
        # Assert
        assert response.status_code == 200
        assert response.json()['message'] == 'Signed up newstudent@mergington.edu for Chess Club'
        assert email in activities['Chess Club']['participants']

    def test_signup_activity_not_found(self):
        # Arrange
        email = 'student@mergington.edu'
        # Act
        response = client.post(f'/activities/Nonexistent/signup?email={email}')
        # Assert
        assert response.status_code == 404
        assert response.json()['detail'] == 'Activity not found'

    def test_signup_already_registered(self):
        # Arrange
        email = 'michael@mergington.edu'
        # Act
        response = client.post(f'/activities/Chess Club/signup?email={email}')
        # Assert
        assert response.status_code == 400
        assert 'already signed up' in response.json()['detail']

class TestUnregisterEndpoint:
    def test_unregister_success(self):
        # Arrange
        email = 'tempstudent@mergington.edu'
        client.post(f'/activities/Chess Club/signup?email={email}')
        # Act
        response = client.delete(f'/activities/Chess Club/signup?email={email}')
        # Assert
        assert response.status_code == 200
        assert response.json()['message'] == f'Unregistered {email} from Chess Club'
        assert email not in activities['Chess Club']['participants']

    def test_unregister_not_signed_up(self):
        # Arrange
        email = 'notregistered@mergington.edu'
        # Act
        response = client.delete(f'/activities/Chess Club/signup?email={email}')
        # Assert
        assert response.status_code == 400
        assert 'not signed up' in response.json()['detail']

    def test_unregister_activity_not_found(self):
        # Arrange
        email = 'student@mergington.edu'
        # Act
        response = client.delete(f'/activities/Nonexistent/signup?email={email}')
        # Assert
        assert response.status_code == 404
        assert response.json()['detail'] == 'Activity not found'
