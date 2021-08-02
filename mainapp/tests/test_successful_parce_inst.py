

def test_successful_parce_inst(api_client_no_auth):
    url = 'http://0.0.0.0:8000/api/uni_temir/parse-inst-account/'
    response = api_client_no_auth.post(url)
    print(response)
    assert response.status_code == 200