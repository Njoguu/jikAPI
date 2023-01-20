template = {
    "swagger" : "2.0",
    "info" : {
        "title" : "jikAPI",
        "description" : "Jobs In Kenya Live API returning most recent job openings in Kenya",
        "contact" : {
            "name": "API Support",
            "url": "https://www.twitter.com/@whoisnjoguu",
            "email" : "bigboydevelops@gmail.com",
        },
        # "termsOfService" : "www.twitter.com/@whoisnjoguu",
        "license" : {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
        },
        "version" : "2.0.1"
    },
    "basePath": "/api/v2/",
    "schemes" : [
        "http",
        "https"
    ]
}

swagger_config = {
    "headers" : [

    ],
    "specs" : [
        {
            "endpoint" : "apispec",
            "route" : "/apispec.json",
            "rule_filter" : lambda rule: True,
            "model_filter" : lambda tag: True,
        }
    ],
    "static_url_path" : "/flassger_static",
    "swagger_ui":True,
    "specs_route" : "/api/v2/"
}