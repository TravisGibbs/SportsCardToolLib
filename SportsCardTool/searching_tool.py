import requests
import json

"""
This file contains the query building class which helps users access data api.
"""

DEV_QUERY = "http://127.0.0.1:5000/api/v1/sportscards/search?"
BASE_QUERY = "https://travisapi.pythonanywhere.com/api/v1/sportscards/search?"


class query_builder:
    """The query_builder class allows for quick queries to SportsCardTool's API

    The API can also be accessed manually for now, but this class helps build queries progmatically.

    Attributes:
        query: A string containing the query to the API
        terms: A int counting the number of terms in query

    """

    def __init__(
        self,
        base: str = BASE_QUERY,
    ) -> None:
        """Intializes the query builder object.

        Args:
            base: The base url of query, defaults to the where the API is currently hosted.
            Do not recommend changing unless performing local development on server.
        """
        self.query = base
        self.terms = 0

    # Possible key value pairs: [name, team, group, set, year, serial, auto, mem, contains]
    # Specify multiple item queries as comma seperated string IE {"name": "Rafael Devers,Juan Soto"}
    # Searching via contains key checks if string is contained in the listing (non-case sensitive)
    def add_item(self, filters: dict):
        """Adds items from a dictionary of key value pairs to the query.

        Key value pairs are parsed into url params. In the future we would like to support
        clauses and conditionals, but currently we support the following:

        Possible keys: [name, team, group, set, year, serial, auto, mem, contains]
        Specify multi value queries as comma seperated string IE {"name": "Rafael Devers,Juan Soto"}
        Searching via contains key checks if string is contained in the listing (non-case sensitive)

        Args:
            filters: A dictionary keyed by term and valued with a string containing all desired values.

        """
        for key, value in filters.items():
            if self.terms == 0:
                self.query += key + "=" + value
            else:
                self.query += "&" + key + "=" + value

            self.terms += 1

    def grab_data(self, min_results: int = 20):
        """Executes query as defined by class atribute.

        Pages through results produced by query string untill
        it hits the min results argument or runs out of data.

        Args:
            min_results: An int specifying how many results at
            a minimum to return.

        Returns:
            A tuples where the first value is a list of dictionarties of results
            and the second value is an int with the total number of results.

        """
        total_results = 0
        results = []
        page = 0

        print("Fetching Results")
        while True:
            q = self.query + "&page=" + str(page)
            r = requests.get(q)

            data = json.loads(r.content)
            results.extend(data["cards"])
            total_results += len(data["cards"])

            # If this is the last page we break
            if (
                data["total_results"] < data["entries_per_page"]
                or total_results >= min_results
            ):
                break

            page += 1

        return (results, total_results)
