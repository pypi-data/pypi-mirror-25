
## Command Line Interface

### Prerequisites
* [python 2.7.9+ or 3.4+](https://www.python.org/downloads/)
* [LeoLabs Platform Account](https://platform.leolabs.space/)

### Installation

pip install leolabs --upgrade

### Configuration

```
$ leolabs configure
Access Key: xxxxx
Secret Key: xxxxx
```

### Examples

List Instruments
```
$ leolabs instruments list
{
    "instruments": [
        {
            "altitude": 213.0, 
            "longitude": -147.47104, 
            "latitude": 65.12992, 
            "transmitFrequency": 450000000.0, 
            "id": "pfisr", 
            "transmitPower": 2000000.0
        }, 
        {
            "altitude": 855.0, 
            "longitude": -103.233245, 
            "latitude": 31.9643, 
            "transmitFrequency": 440000000.0, 
            "id": "msr", 
            "transmitPower": 65000.0
        }
    ]
}
```

Get a Catalog Object by LeoLabs Catalog Number
```
$ leolabs catalog get --catalog-number L72
{
    "name": "ISS (ZARYA)", 
    "noradCatalogNumber": 25544, 
    "catalogNumber": "L72"
}
```

Get a Catalog Object by Norad Catalog Number
```
leolabs catalog get --norad-catalog-number 25544
{
    "name": "ISS (ZARYA)", 
    "noradCatalogNumber": 25544, 
    "catalogNumber": "L72"
}
```

Request Priority Tasking for Catalog Object
```
leolabs catalog create-task --catalog-number L72 \
  --start-time "2017-09-01T03:00:00Z" \
  --end-time "2017-09-01T03:01:00Z"
{
    "id": 27102
}
```

Get Measurements
```
leolabs catalog get-measurements --catalog-number L72 \
  --start-time "2017-08-12T03:07:47Z" \
  --end-time "2017-08-12T03:08:00Z"
{
    "measurements": [
        {
            "group": 1, 
            "noradCatalogNumber": 25544, 
            "instrument": "msr", 
            "measuredAt": "2017-08-12T03:07:47.412846", 
            "updatedAt": "2017-08-12T03:16:07.419895", 
            "corrected": {
                "dopplerError": 1.06436160839311, 
                "doppler": 2780.29290741333, 
                "elevation": 41.5, 
                "rcs": 2.66584545877017, 
                "rangeError": 9.37382332942345, 
                "range": 594267.276276089, 
                "azimuth": 70.5
            }, 
            "transmittedAt": "2017-08-12T03:07:47.410863", 
            "receivedAt": "2017-08-12T03:07:47.414828", 
            "beam": 64259, 
            "experiment": 4810860, 
            "snr": 40.5322113037109, 
            "targetPass": 88300344, 
            "catalogNumber": "L72", 
            "corrections": [
                {
                    "source": "leolabs", 
                    "type": "doppler_bias", 
                    "value": 22.9424441491722, 
                    "error": 0.0607159553394624
                }, 
                {
                    "source": "leolabs", 
                    "type": "range_bias", 
                    "value": 8.71751218254212, 
                    "error": 0.434361784658141
                }, 
                {
                    "source": "iri16", 
                    "type": "ionospheric", 
                    "value": 24.6481534470116
                }
            ], 
            "values": {
                "dopplerError": 0.289238941350412, 
                "doppler": 2803.2353515625, 
                "elevation": 41.5, 
                "rcs": 0.00186994376446691, 
                "rangeError": 23.5445588864603, 
                "range": 594300.641941718, 
                "azimuth": 70.5
            }, 
            "id": 100446008, 
            "integrationTime": 0.185004
        }
    ]
}
```
