import pytest

from ml_data_analysis import (
    get_dataclass, 
    fall_percent, 
    date_distribution, 
    location_mass_distribution, 
    closest_meteorite
)

def test_get_dataclass():
    assert get_dataclass([{'name': 'Meteor1'}, {'name': 'Meteor2'}], 'name') == ['Meteor1', 'Meteor2']
    assert get_dataclass([{'year': 2020}, {'year': 2021}], 'year') == [2020, 2021]

def test_fall_percent():
    assert fall_percent([{'fall': 'Fell'}, {'fall': 'Found'}, {'fall': 'Fell'}]) == (67.0, 33.0)
    assert fall_percent([{'fall': 'Fell'}, {'fall': 'Fell'}, {'fall': 'Fell'}]) == (100.0, 0.0)
    assert fall_percent([{'fall': 'Found'}, {'fall': 'Found'}, {'fall': 'Found'}]) == (0.0, 100.0)
    with pytest.raises(ZeroDivisionError):
        fall_percent([])

def test_date_distribution():
    assert date_distribution([{'year': '1899'}, {'year': '1925'}, {'year': '1950'}, {'year': '1975'}, {'year': '2000'}, {'year': '2010'}])\
          == {'Before 1900': 1, '1900-1925': 1, '1926-1950': 1, '1951-1975': 1, '1976-2000': 1, '2001-2010': 1, 'After 2010': 0}
    assert date_distribution([]) == {'Before 1900': 0, '1900-1925': 0, '1926-1950': 0, '1951-1975': 0, '1976-2000': 0, '2001-2010': 0, 'After 2010': 0}

def location_mass_distribution():
    assert location_mass_distribution([{'reclat': '40.7128', 'reclong': '-74.0060', 'mass (g)': '1000'},
         {'reclat': '34.0522', 'reclong': '-118.2437', 'mass (g)': '2000'},
         {'reclat': '', 'reclong': '-118.2437', 'mass (g)': '500'},
         {'reclat': '37.7749', 'reclong': '', 'mass (g)': '1500'},
         {'reclat': '41.8781', 'reclong': '-87.6298', 'mass (g)': '800'}]) == \
         {
            'Northern & Eastern': 1000.0,
            'Northern & Western': 2000.0,
            'Southern & Eastern': 1500.0,
            'Southern & Western': 800.0
        }
    assert location_mass_distribution([]) == {'Northern & Eastern': 0, 'Northern & Western': 0, 'Southern & Eastern': 0, 'Southern & Western': 0}

def test_closest_meteorite():
    assert closest_meteorite([
            {'id': '1', 'name': 'Meteor1', 'reclat': '0', 'reclong': '0'},
            {'id': '2', 'name': 'Meteor2', 'reclat': '10', 'reclong': '10'},
            {'id': '3', 'name': 'Meteor3', 'reclat': '', 'reclong': ''},
            {'id': '4', 'name': 'Meteor4', 'reclat': '50', 'reclong': '50'},
            {'id': '5', 'name': 'Meteor5', 'reclat': '-50', 'reclong': '-50'}
        ], 1) == \
        (
            {'id': '1', 'name': 'Meteor1', 'reclat': '0', 'reclong': '0'},
            'Meteor2',
            1570.2776641936298
        )
    assert closest_meteorite([{'id': '1', 'name': 'Meteor1', 'reclat': '0', 'reclong': '0'}], 100) == 'Invalid meteorite id'