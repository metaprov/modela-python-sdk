import hashlib

from github.com.metaprov.modelaapi.services.fileservices.v1.fileservices_pb2 import DataBlock
from github.com.metaprov.modelaapi.services.fileservices.v1.fileservices_pb2_grpc import FileServicesServiceStub

from modela import DataLocation


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
        if len(data_block) > 0:
            hash = hashlib.new('md5', str(data_block).encode('utf-8')).hexdigest()
            request = DataBlock(
                name=self.name,
                data=bytes(data_block, encoding='utf-8'),
                md5_hash=str(hash),
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
            raise StopIteration


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
                    resource_name: str) -> DataLocation:
        data_block_iterable = DataBlockRequestIterable(name, data, tenant, data_product,
                                                       version, bucket, resource_name, resource_type)

        print("Uploading file with length {0}".format(len(data)))
        response = self.__stub.UploadChunk(data_block_iterable, timeout=20)
        return DataLocation(BucketName=bucket, Path=response.key)