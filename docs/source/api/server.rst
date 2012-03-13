=================
Tailor Server API
=================


Tailor Command JSON
-------------------

::

    {
        "hosts": [
            "server1.example.com"
        ],
        "commands": [
            {
                "command": "make_release",
                "params": [
                    {
                        "name": "tag",
                        "value": "1.0"
                    },
                    {
                        "name": "message",
                        "value": "a new tag"
                    }
                ]
            },
            {
                "command": "alpha",
                "params": []
            }
        ],
        "api_key": "sdfsdlkoweiu209823f4980fsadnfBQAMCk3I",
        "schema_url": "http://localhost:8001/tailor/api/v1/schema/"
    }