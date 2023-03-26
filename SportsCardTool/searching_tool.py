import requests
import json

DEV_QUERY = "http://127.0.0.1:5000/api/v1/sportscards/search?"
BASE_QUERY = "http://flask-cards-env.eba-gsyr32jx.us-east-2.elasticbeanstalk.com/api/v1/sportscards/search?"


class QueryBuilder:
    def __init__(self) -> None:
        self.query = BASE_QUERY
        self.terms = 0

    # Possible key value pairs: [name, team, group, set, year, serial, auto, mem, contains]
    # Specify multiple item queries as comma seperated string IE {"name": "Rafael Devers,Juan Soto"}
    # Searching via contains key checks if string is contained in the listing (non-case sensitive)
    def add_item(self, dict):
        for key, value in dict.items():
            if self.terms == 0:
                self.query += key + "=" + value
            else:
                self.query += "&" + key + "=" + value

            self.terms += 1

    # Allows for easy access and paging through data API, returns a list of dictionaries
    def grab_data(self, min_results=1000):
        total_results = 0
        results = []
        page = 0

        print("Fetching Results")
        while True:
            q = self.query + "&page=" + str(page)
            r = requests.get(q)

            data = json.loads(r.content)
            results.extend(data['cards'])
            total_results += len(data['cards'])

            # If this is the last page we break
            if data['total_results'] < data["entries_per_page"] or total_results >= min_results:
                break

            page += 1

        return (results, total_results)
