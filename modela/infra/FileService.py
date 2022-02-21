import hashlib

from github.com.metaprov.modelaapi.services.fileservices.v1.fileservices_pb2 import DataBlock
from github.com.metaprov.modelaapi.services.fileservices.v1.fileservices_pb2_grpc import FileServicesServiceStub


class DataBlockRequestIterable(object):
    BLOCK_SIZE = 20000

    def __init__(self, name: str,
                 data: bytes,
                 tenant: str,
                 data_product: str,
                 version: str,
                 bucket: str,
                 resource_type: str,
                 resource_name: str):

        self.name = name
        self.data = data
        self.tenant = tenant
        self.data_product = data_product
        self.version = version
        self.bucket = bucket
        self.resource_type = resource_type
        self.resource_name = resource_name
        self.loc = 0

    def __iter__(self):
        return self

    def __next__(self):
        data_block = self.data[self.loc:self.loc + self.BLOCK_SIZE]
        if data_block:
            hash = hashlib.new('md5', data_block).hexdigest()
            request = DataBlock(
                name=self.name,
                data="",
                md5_hash=hash,
                tenant=self.tenant,
                dataProductName=self.data_product,
                dataProductVersion=self.version,
                bucket=self.bucket,
                resourceType=self.resource_type,
                resourceName=self.resource_name
            )
            self.loc += self.BLOCK_SIZE
            return request
        else:
            return StopIteration


class FileService:
    def __init__(self, stub):
        self.__stub: FileServicesServiceStub = stub

    def upload_file(self,
                    name: str,
                    data: bytes,
                    tenant: str,
                    data_product: str,
                    version: str,
                    bucket: str,
                    resource_type: str,
                    resource_name: str):
        data_block_iterable = DataBlockRequestIterable(name, data, tenant, data_product,
                                                       version, bucket, resource_name, resource_type)
        response = self.__stub.UploadChunk(data_block_iterable)
