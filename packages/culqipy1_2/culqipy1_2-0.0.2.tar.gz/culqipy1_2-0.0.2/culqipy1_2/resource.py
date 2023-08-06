from culqipy1_2.utils import RequestMethodError, Util


class Operation():

    @staticmethod
    def list(url, params=None, key=None):
        return Util(
            url=url,
            data=params,
            method="GET",
            key=key,
        ).json_result()

    @staticmethod
    def create(url, body, key=None):
        return Util(
            url=url,
            data=body,
            method="POST",
            key=key,
        ).json_result()

    @staticmethod
    def get_delete(url, id, method, key=None):
        """
        Get or delete, just change the method: "GET" or "DELETE".
        """
        return Util(
            url=url + id + "/",
            method=method,
            key=key,
        ).json_result()


class BaseResource:
    """Parent class for all the resources."""

    URL = None

    @classmethod
    def crear(cls, body):
        return Operation.create(cls.URL, body)


class Cargo(BaseResource):

    URL = "/cargos"


class Plan(BaseResource):

    URL = "/planes"


class Suscripcions(BaseResource):

    URL = "/suscripciones"
