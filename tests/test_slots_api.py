import requests
import pytest

root_url = "http://127.0.0.1:5000"

# Setup for the tests. requesting access token for login
@pytest.fixture(scope='module')
def access_token(request):
    response = requests.post(root_url + '/login', data={'username': 'admin', 'password': 'admin123'})
    return response.json().get('access_token', '')


class TestGetAllSlots:
    # Here we make the fixture available inside the class.
    @pytest.fixture(autouse=True)
    def _request_access_token(self, access_token):
        self._response = access_token

    def test_slots(self):
        req = requests.get(root_url + '/api/v1.0/slots',
                           headers={'Authorization': 'Bearer ' + self._response})
        assert req.status_code == 200
