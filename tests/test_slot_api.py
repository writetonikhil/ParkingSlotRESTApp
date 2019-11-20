import pytest
import requests

root_url = "http://127.0.0.1:5000"


# Setup for the tests. requesting access token for login
@pytest.fixture(scope='module')
def access_token(request):
    response = requests.post(root_url + '/login', data={'username': 'admin', 'password': 'admin123'})
    return response.json().get('access_token', '')


class TestPOSTPositive:

    # Here we make the fixture available inside the class.
    @pytest.fixture(autouse=True)
    def _request_access_token(self, access_token):
        self._response = access_token

    def test_slot_create(self):
        resp = requests.post(root_url + '/api/v1.0/slots/' + '1',
                             data={'available': False},
                             headers={'Authorization': 'Bearer ' + self._response}
                             )
        print(resp.text)
        assert resp.status_code == 201


class TestGetPositive:
    # Here we make the fixture available inside the class.
    @pytest.fixture(autouse=True)
    def _request_access_token(self, access_token):
        self._response = access_token

    def test_slot_get_by_id(self):
        assert requests.get(root_url + '/api/v1.0/slots/' + '1',
                            headers={'Authorization': 'Bearer ' + self._response}
                            ).status_code == 200


class TestPUTPositive:
    # Here we make the fixture available inside the class.
    @pytest.fixture(autouse=True)
    def _request_access_token(self, access_token):
        self._response = access_token

    def test_slot_occupy_slot(self):
        assert requests.put(root_url + '/api/v1.0/slots/' + '1',
                            data= {'available': False},
                            headers={'Authorization': 'Bearer ' + self._response}).status_code == 200

    def test_slot_release_slot(self):
        assert requests.put(root_url + '/api/v1.0/slots/' + '1',
                            data={'available': True},
                            headers={'Authorization': 'Bearer ' + self._response}).status_code == 200


class TestPUTNegative:
    # Here we make the fixture available inside the class.
    @pytest.fixture(autouse=True)
    def _request_access_token(self, access_token):
        self._response = access_token

    def test_slot_wrong_arg_type(self):
        mydata = {'available': 10}
        response = requests.put(root_url + '/api/v1.0/slots/' + '1',
                                data=mydata,
                                headers={'Authorization': 'Bearer ' + self._response})
        with pytest.raises(requests.exceptions.HTTPError) as err_msg:
            response.raise_for_status()
        print("Error: %s" % repr(err_msg.value))
        print("Traceback: %s" % str(err_msg.traceback))


class TestDELETEPositive:
    # Here we make the fixture available inside the class.
    @pytest.fixture(autouse=True)
    def _request_access_token(self, access_token):
        self._response = access_token

    def test_slot_delete(self):
        assert requests.delete(root_url + '/api/v1.0/slots/' + '1',
                               headers={'Authorization': 'Bearer ' + self._response}).status_code == 200


class TestDELETENegative:
    # Here we make the fixture available inside the class.
    @pytest.fixture(autouse=True)
    def _request_access_token(self, access_token):
        self._response = access_token

    def test_non_existing_slot_delete(self):
        response = requests.delete(root_url + '/api/v1.0/slots/' + '100',
                                   headers={'Authorization': 'Bearer ' + self._response})
        with pytest.raises(requests.exceptions.HTTPError) as err_msg:
            response.raise_for_status()
        print("Error: %s" % repr(err_msg.value))
        print("Traceback: %s" % str(err_msg.traceback))


class TestGetNegative:
    # Here we make the fixture available inside the class.
    @pytest.fixture(autouse=True)
    def _request_access_token(self, access_token):
        self._response = access_token

    def test_slot_get_by_id_error(self):
        response = requests.get(root_url + '/api/v1.0/slots/' + '1',
                                headers={'Authorization': 'Bearer ' + self._response})
        with pytest.raises(requests.exceptions.HTTPError) as err_msg:
            response.raise_for_status()
        print("Error: %s" % repr(err_msg.value))
        print("Traceback: %s" % str(err_msg.traceback))

    def test_slot_get_by_id_str(self):
        response = requests.get(root_url + '/api/v1.0/slots/' + 'a',
                                headers={'Authorization': 'Bearer ' + self._response})
        with pytest.raises(requests.exceptions.HTTPError) as err_msg:
            response.raise_for_status()
        print("Error: %s" % str(err_msg.value))
        print("Traceback: %s" % str(err_msg.traceback))
