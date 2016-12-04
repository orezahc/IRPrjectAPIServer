#### API to get a nouns from a sentence using nltk package in python

##### build up the docker image and run in the docker container
```
cd IRProjectAPIServer
docker build -t irppj-google:latest .
docker-compose up [-d]
```
##### api is ready in port 80

api: <ipaddress>/<restaurant-name>

expected request: 
```
{
    "medata": {
	"keyword": "restaurantName",
                "timestamp" : int(time.time())
            },
            "data": [
                {
                    "contact": {
                        "address": "411 University St, Seattle, WA 98101, USA",
                        "phone": "(206) 621-1700",
                        "url": "https://maps.google.com/?cid=15936259808444107162"
                    },
                    "geometry": {
                        "lat": 47.6080596,
                        "lng": -122.3339349
                    },
                    "name": "Fairmont Olympic Hotel, Seattle",
                    "open": True,
                    "price": 4.0,
                    "rating": 4.5
                }
            ]
        }
}
```
