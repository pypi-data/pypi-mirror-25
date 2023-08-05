import aiobotocore
from pynamodb.constants import (
    RETURN_CONSUMED_CAPACITY_VALUES, RETURN_ITEM_COLL_METRICS_VALUES, COMPARISON_OPERATOR_VALUES,
    RETURN_ITEM_COLL_METRICS, RETURN_CONSUMED_CAPACITY, RETURN_VALUES_VALUES, ATTR_UPDATE_ACTIONS,
    COMPARISON_OPERATOR, EXCLUSIVE_START_KEY, SCAN_INDEX_FORWARD, SCAN_FILTER_VALUES, ATTR_DEFINITIONS,
    BATCH_WRITE_ITEM, CONSISTENT_READ, ATTR_VALUE_LIST, DESCRIBE_TABLE, KEY_CONDITIONS,
    BATCH_GET_ITEM, DELETE_REQUEST, SELECT_VALUES, RETURN_VALUES, REQUEST_ITEMS, ATTR_UPDATES,
    ATTRS_TO_GET, SERVICE_NAME, DELETE_ITEM, PUT_REQUEST, UPDATE_ITEM, SCAN_FILTER, TABLE_NAME,
    INDEX_NAME, KEY_SCHEMA, ATTR_NAME, ATTR_TYPE, TABLE_KEY, EXPECTED, KEY_TYPE, GET_ITEM, UPDATE,
    PUT_ITEM, SELECT, ACTION, EXISTS, VALUE, LIMIT, QUERY, SCAN, ITEM, LOCAL_SECONDARY_INDEXES,
    KEYS, KEY, EQ, SEGMENT, TOTAL_SEGMENTS, CREATE_TABLE, PROVISIONED_THROUGHPUT, READ_CAPACITY_UNITS,
    WRITE_CAPACITY_UNITS, GLOBAL_SECONDARY_INDEXES, PROJECTION, EXCLUSIVE_START_TABLE_NAME, TOTAL,
    DELETE_TABLE, UPDATE_TABLE, LIST_TABLES, GLOBAL_SECONDARY_INDEX_UPDATES,
    CONSUMED_CAPACITY, CAPACITY_UNITS, QUERY_FILTER, QUERY_FILTER_VALUES, CONDITIONAL_OPERATOR,
    CONDITIONAL_OPERATORS, NULL, NOT_NULL, SHORT_ATTR_TYPES, DELETE,
    ITEMS, DEFAULT_ENCODING, BINARY_SHORT, BINARY_SET_SHORT, LAST_EVALUATED_KEY, RESPONSES, UNPROCESSED_KEYS,
    UNPROCESSED_ITEMS, STREAM_SPECIFICATION, STREAM_VIEW_TYPE, STREAM_ENABLED)
BOTOCORE_EXCEPTIONS = (BotoCoreError, ClientError)


class Connection:
    service_name = 'dynamodb'

    def __init__(self, region_name, host=None):
        self.session = aiobotocore.get_session()
        self._client = None
        self._tables = {}

    def create_client(self):
        return self.session.create_client(
            self.service_name, region_name=self.region_name
        )

    @property
    def client(self):
        if self._client is None:
            self._client = self.create_client()
        return self._client

    async def get_item(self,
                       table_name,
                       hash_key,
                       range_key=None,
                       consistent_read=False,
                       attributes_to_get=None):
        operation_kwargs = {}
        if attributes_to_get is not None:
            operation_kwargs[ATTRS_TO_GET] = attributes_to_get
        operation_kwargs[CONSISTENT_READ] = consistent_read
        operation_kwargs[TABLE_NAME] = table_name
        operation_kwargs.update(
            self.get_identifier_map(table_name, hash_key, range_key)
        )
        return await self.client.get_item(
        try:
            return self.dispatch(GET_ITEM, operation_kwargs)
        except BOTOCORE_EXCEPTIONS as e:
            raise GetError("Failed to get item: {0}".format(e), e)

    def get_identifier_map(self, table_name, hash_key, range_key=None, key=KEY):
        """
        Builds the identifier map that is common to several operations
        """
        tbl = self.get_meta_table(table_name)
        if tbl is None:
            raise TableError("No such table {0}".format(table_name))
        return tbl.get_identifier_map(hash_key, range_key=range_key, key=key)

    def get_meta_table(self, table_name, refresh=False):
        """
        Returns a MetaTable
        """
        if table_name not in self._tables or refresh:
            operation_kwargs = {
                TABLE_NAME: table_name
            }
            try:
                data = self.dispatch(DESCRIBE_TABLE, operation_kwargs)
                self._tables[table_name] = MetaTable(data.get(TABLE_KEY))
            except BotoCoreError as e:
                raise TableError("Unable to describe table: {0}".format(e), e)
            except ClientError as e:
                if 'ResourceNotFound' in e.response['Error']['Code']:
                    raise TableDoesNotExist(e.response['Error']['Message'])
                else:
                    raise
        return self._tables[table_name]

    async def dispatch(self, operation_name, operation_kwargs):
        if
