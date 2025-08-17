# Ejemplo para utils/network_helpers.py
@patch("requests.get")
def test_fetch_url(self, mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "mock data"
    result = fetch_url("http://test.com")
    self.assertEqual(result, "mock data")
