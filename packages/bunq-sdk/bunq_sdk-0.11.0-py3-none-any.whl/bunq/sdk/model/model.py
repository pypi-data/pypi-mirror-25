from bunq.sdk import client
from bunq.sdk import context
from bunq.sdk.json import converter


class BunqModel(object):
    # Field constants
    _FIELD_RESPONSE = 'Response'
    _FIELD_PAGINATION = 'Pagination'
    _FIELD_ID = 'Id'
    _FIELD_UUID = 'Uuid'

    # The very first index of an array
    _INDEX_FIRST = 0

    def to_json(self):
        """
        :rtype: str
        """

        return converter.class_to_json(self)

    @classmethod
    def _from_json_array_nested(cls, response_raw):
        """
        :type response_raw: client.BunqResponseRaw

        :rtype: bunq.sdk.client.BunqResponse[cls]
        """

        json = response_raw.body_bytes.decode()
        obj = converter.json_to_class(dict, json)
        value = converter.deserialize(cls, obj[cls._FIELD_RESPONSE])

        return client.BunqResponse(value, response_raw.headers)

    @classmethod
    def _from_json(cls, response_raw, wrapper=None):
        """
        :type response_raw: client.BunqResponseRaw
        :type wrapper: str|None

        :rtype: client.BunqResponse[cls]
        """

        json = response_raw.body_bytes.decode()
        obj = converter.json_to_class(dict, json)
        value = converter.deserialize(
            cls,
            cls._unwrap_response_single(obj, wrapper)
        )

        return client.BunqResponse(value, response_raw.headers)

    @classmethod
    def _unwrap_response_single(cls, obj, wrapper=None):
        """
        :type obj: dict
        :type wrapper: str|None

        :rtype: dict
        """

        if wrapper is not None:
            return obj[cls._FIELD_RESPONSE][cls._INDEX_FIRST][wrapper]

        return obj[cls._FIELD_RESPONSE][cls._INDEX_FIRST]

    @classmethod
    def _process_for_id(cls, response_raw):
        """
        :type response_raw: client.BunqResponseRaw

        :rtype: client.BunqResponse[int]
        """

        json = response_raw.body_bytes.decode()
        obj = converter.json_to_class(dict, json)
        id_ = converter.deserialize(
            Id,
            cls._unwrap_response_single(obj, cls._FIELD_ID)
        )

        return client.BunqResponse(id_.id_, response_raw.headers)

    @classmethod
    def _process_for_uuid(cls, response_raw):
        """
        :type response_raw: client.BunqResponseRaw

        :rtype: client.BunqResponse[str]
        """

        json = response_raw.body_bytes.decode()
        obj = converter.json_to_class(dict, json)
        uuid = converter.deserialize(
            Uuid,
            cls._unwrap_response_single(obj, cls._FIELD_UUID)
        )

        return client.BunqResponse(uuid.uuid, response_raw.headers)

    @classmethod
    def _from_json_list(cls, response_raw, wrapper=None):
        """
        :type response_raw: client.BunqResponseRaw
        :type wrapper: str|None

        :rtype: client.BunqResponse[list[cls]]
        """

        json = response_raw.body_bytes.decode()
        obj = converter.json_to_class(dict, json)
        array = obj[cls._FIELD_RESPONSE]
        array_deserialized = []

        for item in array:
            item_unwrapped = item if wrapper is None else item[wrapper]
            item_deserialized = converter.deserialize(cls, item_unwrapped)
            array_deserialized.append(item_deserialized)

        pagination = converter.deserialize(client.Pagination,
                                           obj[cls._FIELD_PAGINATION])

        return client.BunqResponse(array_deserialized, response_raw.headers,
                                   pagination)


class Id(BunqModel):
    """
    :type _id_: int
    """

    def __init__(self):
        self._id_ = None

    @property
    def id_(self):
        """
        :rtype: int
        """

        return self._id_


class Uuid(BunqModel):
    """
    :type _uuid: str
    """

    def __init__(self):
        self._uuid = None

    @property
    def uuid(self):
        """
        :rtype: str
        """

        return self._uuid


class SessionToken(BunqModel):
    """
    :type _id_: int
    :type _created: str
    :type _updated: str
    :type _token: str
    """

    def __init__(self):
        self._id_ = None
        self._created = None
        self._updated = None
        self._token = None

    @property
    def id_(self):
        """
        :rtype: int
        """

        return self._id_

    @property
    def created(self):
        """
        :rtype: str
        """

        return self._created

    @property
    def updated(self):
        """
        :rtype: str
        """

        return self._updated

    @property
    def token(self):
        """
        :rtype: str
        """

        return self._token


class PublicKeyServer(BunqModel):
    """
    :type _server_public_key: str
    """

    def __init__(self):
        self._server_public_key = None

    @property
    def server_public_key(self):
        """
        :rtype: str
        """

        return self._server_public_key


class Installation(BunqModel):
    """
    :type _id_: Id
    :type _token: SessionToken
    :type _server_public_key: PublicKeyServer
    """

    # Endpoint name.
    _ENDPOINT_URL_POST = "installation"

    # Field constants.
    FIELD_CLIENT_PUBLIC_KEY = "client_public_key"

    def __init__(self):
        self._id_ = None
        self._token = None
        self._server_public_key = None

    @property
    def id_(self):
        """
        :rtype: Id
        """

        return self._id_

    @property
    def token(self):
        """
        :rtype: SessionToken
        """

        return self._token

    @property
    def server_public_key(self):
        """
        :rtype: PublicKeyServer
        """

        return self._server_public_key

    @classmethod
    def create(cls, api_context, public_key_string):
        """
        :type api_context: context.ApiContext
        :type public_key_string: str

        :rtype: client.BunqResponse[Installation]
        """

        api_client = client.ApiClient(api_context)
        body_bytes = cls.generate_request_body_bytes(
            public_key_string
        )
        response_raw = api_client.post(cls._ENDPOINT_URL_POST, body_bytes, {})

        return cls._from_json_array_nested(response_raw)

    @classmethod
    def generate_request_body_bytes(cls, public_key_string):
        """
        :type public_key_string: str

        :rtype: bytes
        """

        return converter.class_to_json(
            {
                cls.FIELD_CLIENT_PUBLIC_KEY: public_key_string,
            }
        ).encode()


class SessionServer(BunqModel):
    """
    :type _id_: Id
    :type _token: SessionToken
    :type _user_person: bunq.sdk.model.generated.UserPerson
    :type _user_company: bunq.sdk.model.generated.UserCompany
    """

    # Endpoint name.
    _ENDPOINT_URL_POST = "session-server"

    # Field constants
    FIELD_SECRET = "secret"

    def __init__(self):
        self._id_ = None
        self._token = None
        self._user_person = None
        self._user_company = None

    @property
    def id_(self):
        """
        :rtype: Id
        """

        return self._id_

    @property
    def token(self):
        """
        :rtype: SessionToken
        """

        return self._token

    @property
    def user_person(self):
        """
        :rtype: bunq.sdk.model.generated.UserPerson
        """

        return self._user_person

    @property
    def user_company(self):
        """
        :rtype: bunq.sdk.model.generated.UserCompany
        """

        return self._user_company

    @classmethod
    def create(cls, api_context):
        """
        :type api_context: context.ApiContext

        :rtype: client.BunqResponse[SessionServer]
        """

        api_client = client.ApiClient(api_context)
        body_bytes = cls.generate_request_body_bytes(api_context.api_key)
        response_raw = api_client.post(cls._ENDPOINT_URL_POST, body_bytes, {})

        return cls._from_json_array_nested(response_raw)

    @classmethod
    def generate_request_body_bytes(cls, secret):
        """
        :type secret: str

        :rtype: bytes
        """

        return converter.class_to_json({cls.FIELD_SECRET: secret}).encode()


