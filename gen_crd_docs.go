package main

import (
	//"bytes"
	"fmt"
	"gopkg.in/yaml.v2"
	//	"io"
	"io/ioutil"
	"log"
	"os"
	//	"os/exec"
	"path/filepath"
	//	"regexp"
	"strings"
)

const BASE_PY = `./modela/`
const BASE_API_FOLDER = `./manifests/base/crd`

const TEMPLATE = `import grpc
from github.com.metaprov.modelaapi.pkg.apis.%s.v1alpha1.generated_pb2 import DataProduct as MDDataProduct
from github.com.metaprov.modelaapi.services.dataproduct.v1.dataproduct_pb2_grpc import DataProductServiceStub
from github.com.metaprov.modelaapi.services.dataproduct.v1.dataproduct_pb2 import CreateDataProductRequest, \
    UpdateDataProductRequest, \
    DeleteDataProductRequest, GetDataProductRequest, ListDataProductsRequest

from modela.Resource import Resource
from modela.ModelaException import ModelaException
from typing import List, Union


class DataProduct(Resource):
    def __init__(self, item: MDDataProduct = MDDataProduct(), client=None, namespace="", name=""):
        super().__init__(item, client, namespace=namespace, name=name)


class DataProductClient:
    def __init__(self, stub):
        self.__stub: DataProductServiceStub = stub

    def create(self, dataproduct: DataProduct) -> bool:
        request = CreateDataProductRequest()
        request.dataproduct.CopyFrom(dataproduct.raw_message)
        try:
            response = self.__stub.CreateDataProduct(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def update(self, dataproduct: DataProduct) -> bool:
        request = UpdateDataProductRequest()
        request.dataproduct.CopyFrom(dataproduct.raw_message)
        try:
            self.__stub.UpdateDataProduct(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def get(self, namespace: str, name: str) -> Union[DataProduct, bool]:
        request = GetDataProductRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.GetDataProduct(request)
            return DataProduct(response.dataproduct, self)
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def delete(self, namespace: str, name: str) -> bool:
        request = DeleteDataProductRequest()
        request.namespace = namespace
        request.name = name
        try:
            response = self.__stub.DeleteDataProduct(request)
            return True
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False

    def list(self, namespace: str) -> Union[List[DataProduct], bool]:
        request = ListDataProductsRequest()
        request.namespace = namespace
        try:
            response = self.__stub.ListDataProducts(request)
            return [DataProduct(item, self) for item in response.dataproducts.items]
        except grpc.RpcError as err:
            error = err

        ModelaException.process_error(error)
        return False


`

func main() {
	files, err := ioutil.ReadDir(BASE_API_FOLDER)
	if err != nil {
		log.Fatal(err)
	}

	var path, _ = os.Getwd()

	for _, f := range files {
		var name = f.Name()
		if name == "kustomization" { continue }
        if strings.Contains(name, "catalog") { continue }
        if strings.Contains(name, "datasource") { continue }
		if strings.Contains(name, "dataset") { continue }
		if strings.Contains(name, "dataproduct") { continue }


		fields := strings.Split(name, ".")
		data, err := ioutil.ReadFile(filepath.Join(path, BASE_API_FOLDER, name))
		type yam interface{}
		var yml yam
		yaml.Unmarshal(data, &yml)
		upper := (yml.(map[interface{}]interface{})["spec"]).(map[interface{}]interface{})["names"].(map[interface{}]interface{})["kind"].(string)
		lower := strings.ToLower(upper)
		replacer := strings.NewReplacer("DataProduct", upper, "dataproduct", lower)
		if len(fields) != 4 { continue }
		file, err := os.OpenFile(fmt.Sprintf("%s.py", filepath.Join(path, BASE_PY, fields[0], upper)), os.O_CREATE|os.O_RDWR, 0644)
		if err != nil {
			log.Printf("docs file for %s not found. skipping", name)
			continue
		}

		template := fmt.Sprintf(TEMPLATE, fields[0])
		template = replacer.Replace(template)

		file.Truncate(0)
		file.Seek(0, 0)
		file.Write([]byte(template))
		file.Sync()
		file.Close()
	}
}