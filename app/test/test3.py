import json

data =   '''{
  "resourceMetrics": [
    {
      "resource": {
        "attributes": [
          {
            "key": "host.name",
            "value": {
              "stringValue": "fedora"
            }
          },
          {
            "key": "os.type",
            "value": {
              "stringValue": "linux"
            }
          }
        ]
      },
      "scopeMetrics": [
        {
          "scope": {
            "name": "otelcol/hostmetricsreceiver/load",
            "version": "0.69.0"
          },
          "metrics": [
            {
              "name": "system.cpu.load_average.15m",
              "description": "Average CPU Load over 15 minutes.",
              "unit": "1",
              "gauge": {
                "dataPoints": [
                  {
                    "startTimeUnixNano": "1673272304000000000",
                    "timeUnixNano": "1673655128483269236",
                    "asDouble": 0.27
                  }
                ]
              }
            },
            {
              "name": "system.cpu.load_average.1m",
              "description": "Average CPU Load over 1 minute.",
              "unit": "1",
              "gauge": {
                "dataPoints": [
                  {
                    "startTimeUnixNano": "1673272304000000000",
                    "timeUnixNano": "1673655128483269236",
                    "asDouble": 0.17
                  }
                ]
              }
            },
            {
              "name": "system.cpu.load_average.5m",
              "description": "Average CPU Load over 5 minutes.",
              "unit": "1",
              "gauge": {
                "dataPoints": [
                  {
                    "startTimeUnixNano": "1673272304000000000",
                    "timeUnixNano": "1673655128483269236",
                    "asDouble": 0.37
                  }
                ]
              }
            }
          ]
        }
      ],
      "schemaUrl": "https://opentelemetry.io/schemas/1.9.0"
    },
    {
      "resource": {
        "attributes": [
          {
            "key": "host.name",
            "value": {
              "stringValue": "fedora2"
            }
          },
          {
            "key": "os.type",
            "value": {
              "stringValue": "linux"
            }
          }
        ]
      },
      "scopeMetrics": [
        {
          "scope": {
            "name": "otelcol/hostmetricsreceiver/memory",
            "version": "0.69.0"
          },
          "metrics": [
            {
              "name": "system.memory.usage",
              "description": "Bytes of memory in use.",
              "unit": "By",
              "sum": {
                "dataPoints": [
                  {
                    "startTimeUnixNano": "1673272304000000000",
                    "timeUnixNano": "1673655128483476583",
                    "asInt": "4644356096",
                    "attributes": [
                      {
                        "key": "state",
                        "value": {
                          "stringValue": "used"
                        }
                      }
                    ]
                  },
                  {
                    "startTimeUnixNano": "1673272304000000000",
                    "timeUnixNano": "1673655128483476583",
                    "asInt": "237981696",
                    "attributes": [
                      {
                        "key": "state",
                        "value": {
                          "stringValue": "free"
                        }
                      }
                    ]
                  },
                  {
                    "startTimeUnixNano": "1673272304000000000",
                    "timeUnixNano": "1673655128483476583",
                    "asInt": "81920",
                    "attributes": [
                      {
                        "key": "state",
                        "value": {
                          "stringValue": "buffered"
                        }
                      }
                    ]
                  },
                  {
                    "startTimeUnixNano": "1673272304000000000",
                    "timeUnixNano": "1673655128483476583",
                    "asInt": "1296396288",
                    "attributes": [
                      {
                        "key": "state",
                        "value": {
                          "stringValue": "cached"
                        }
                      }
                    ]
                  },
                  {
                    "startTimeUnixNano": "1673272304000000000",
                    "timeUnixNano": "1673655128483476583",
                    "asInt": "99762176",
                    "attributes": [
                      {
                        "key": "state",
                        "value": {
                          "stringValue": "slab_reclaimable"
                        }
                      }
                    ]
                  },
                  {
                    "startTimeUnixNano": "1673272304000000000",
                    "timeUnixNano": "1673655128483476583",
                    "asInt": "198377472",
                    "attributes": [
                      {
                        "key": "state",
                        "value": {
                          "stringValue": "slab_unreclaimable"
                        }
                      }
                    ]
                  }
                ],
                "aggregationTemporality": "AGGREGATION_TEMPORALITY_CUMULATIVE"
              }
            }
          ]
        }
      ],
      "schemaUrl": "https://opentelemetry.io/schemas/1.9.0"
    }
  ]
}'''



metric_list = []

#jdata = json.loads(data)

#print(jdata)

#print(jdata["resourceMetrics"][0]["resource"]["attributes"])

'''
for i in jdata["resourceMetrics"]:
    timestamp = None
    host = None
    attributes = i["resource"]["attributes"]
    metrics = i["scopeMetrics"]

    for i in attributes:
        if i["key"] == "host.name":
            host = i["value"]["stringValue"]

    for i in metrics:
        print(host, attributes, i["metrics"][0], "\n")
'''



jdata = json.loads(str(data))
for i in jdata["resourceMetrics"]:
    hostname = None
    resource = i["resource"]
    scopemetrics = i["scopeMetrics"]
    for i in resource["attributes"]:
        if i["key"] == "host.name":
            hostname = i["value"]["stringValue"]
    for i in scopemetrics:
        resource = json.dumps(resource)
        scopemetrics = json.dumps(i)
        print(hostname, resource, scopemetrics, "\n")




jdata = json.loads(str(data))
for i in jdata["resourceMetrics"]:
    hostname = None
    resource = i["resource"]
    scopemetrics = i["scopeMetrics"]
    for i in resource["attributes"]:
        dict = i["value"]
        values = list(dict.values())
        if len(values)>1:
            print(i["key"], ':', values)
        else:
            print(i["key"], ':', values[0])
