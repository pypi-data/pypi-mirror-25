import requests
import json


class Client:
    """
    Client class to query to the Powererp backend
    """

    def __init__(self, url, token):
        """
        Class constructor
        :param url: Base URL of the backend
        :type url: str
        :param token:
        :type token:
        """

        self.backend_url = url
        self.token = token

    def method(self, model, identifier, method_name, arguments):
        """
        Calls a method of model

        :param model: Model
        :type model: str
        :param identifier: Id of the element
        :type model: str,int
        :param method_name: Method of the mode
        :type method_name: str
        :param arguments: Arguments to pass to the method
        :type arguments: list
        :return: Result
        :rtype: dict
        """

        built_url = "{}/{}/{}/{}".format(self.backend_url, model, str(identifier), method_name)
        headers = {"Authorization": "token {}".format(self.token)}
        response = requests.post(
            built_url,
            headers=headers,
            params={"args": arguments}
        )
        if response:
            return json.loads(response.content)

    def search(self, model, schema, model_filter):
        """
        Search on the backend
        :param model: Model where search
        :type model: str
        :param schema: Fields to search
        :type schema: list
        :param model_filter: Filter to apply to the model
        :type model_filter: list
        :return: None if there is no response from the backend
        :rtype: None, dict
        """
        
        url = "{}/{}".format(self.backend_url, model)
        headers = {
            "Authorization": "token {}".format(self.token),
            'Content-Type': 'application/json',
        }
        response = requests.get(
            url,
            headers=headers,
            json={
                "filter": json.dumps(model_filter),
                "schema": ','.join(schema)
            }
        )
        return json.loads(response.content)

    def write(self, model, identifier, fields):
        """
        Write on a model

        :param model: Model to write
        :type model: str
        :param identifier: id of the element to write
        :type identifier: int
        :param fields: Data to write
        :type fields: dict
        :return: None
        """

        url = "{}/{}/{}".format(self.backend_url, model, identifier)
        headers = {
            "Authorization": "token {}".format(self.token),
            'Content-Type': 'application/json',
        }
        requests.patch(
            url,
            json.dumps(fields),
            headers=headers
        )

    def create(self, model, fields):
        """
        Creates a record on the model

        :param model:Model name
        :type model: str
        :param fields: data to create the record
        :type fields: dict
        :return: id
        :rtype: int,
        """

        url = "{}/{}".format(self.backend_url, model)
        headers = {
            "Authorization": "token {}".format(self.token),
            'Content-Type': 'application/json',
        }
        response = requests.post(
            url,
            json.dumps(fields),
            headers=headers
        )
        if response.status_code != 200:
            raise Exception(response.content)
        id = json.loads(response.content)["id"]
        return id


