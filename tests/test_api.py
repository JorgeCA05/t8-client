import pytest
import json
from unittest.mock import patch
from datetime import datetime, timezone, UTC
from t8_client.api import obtain_wave, obtain_spectra, obtain_waves, obtain_spectras

# Cargar datos de prueba desde archivos JSON
@pytest.fixture
def mock_wave_data():
    with open('tests/data/mock_wave_data.json') as f:
        return json.load(f)

@pytest.fixture
def mock_spectra_data():
    with open('tests/data/mock_spectra_data.json') as f:
        return json.load(f)

# Mock context
class MockContext:
    obj = {
        'HOST': 'mock_host',
        'USER': 'mock_user',
        'PASSWORD': 'mock_password'
    }

@pytest.fixture
def mock_ctx():
    return MockContext()

def calculate_timestamp(date_str):
    fecha_hora = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
    utc_time = fecha_hora.replace(tzinfo=UTC)
    return int(utc_time.timestamp())

@patch('t8_client.api.requests.get')
def test_obtain_wave(mock_get, mock_ctx, mock_wave_data):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_wave_data
    date_str = '2023-10-28T00:04:16'
    timestamp = calculate_timestamp(date_str)
    result = obtain_wave(mock_ctx, 'machine', 'point', 'pmode', date_str)
    assert result == mock_wave_data
    mock_get.assert_called_once_with(
        f'https://mock_host/rest/waves/machine/point/pmode/{timestamp}',
        auth=('mock_user', 'mock_password')
    )


@patch('t8_client.api.requests.get')
def test_obtain_spectra(mock_get, mock_ctx, mock_spectra_data):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_spectra_data
    date_str = '2023-10-28T00:04:16'
    timestamp = calculate_timestamp(date_str)
    result = obtain_spectra(mock_ctx, 'machine', 'point', 'pmode', date_str)
    assert result == mock_spectra_data
    mock_get.assert_called_once_with(
        f'https://mock_host/rest/spectra/machine/point/pmode/{timestamp}',
        auth=('mock_user', 'mock_password')
    )

@patch('t8_client.api.requests.get')
def test_obtain_waves(mock_get, mock_ctx):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'_items': [{'_links': {'self': 'link1'}}, {'_links': {'self': 'link2'}}]}
    result = obtain_waves(mock_ctx, 'machine', 'point', 'pmode')
    assert result == ['link1', 'link2']
    mock_get.assert_called_once_with(
        'https://mock_host/rest/waves/machine/point/pmode',
        auth=('mock_user', 'mock_password')
    )

@patch('t8_client.api.requests.get')
def test_obtain_spectras(mock_get, mock_ctx):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'_items': [{'_links': {'self': 'link1'}}, {'_links': {'self': 'link2'}}]}
    result = obtain_spectras(mock_ctx, 'machine', 'point', 'pmode')
    assert result == ['link1', 'link2']
    mock_get.assert_called_once_with(
        'https://mock_host/rest/spectra/machine/point/pmode',
        auth=('mock_user', 'mock_password')
    )