from typing import Optional
from grpc import (  # type: ignore
    UnaryUnaryClientInterceptor,
    UnaryStreamClientInterceptor,
    StreamUnaryClientInterceptor,
    StreamStreamClientInterceptor,
)


from github.com.metaprov.modelaapi.services.datapipelinerun.v1 import datapipelinerun_pb2_grpc
from github.com.metaprov.modelaapi.services.datapipeline.v1 import datapipeline_pb2_grpc
from github.com.metaprov.modelaapi.services.dataproduct.v1 import dataproduct_pb2_grpc
from github.com.metaprov.modelaapi.services.dataproductversion.v1 import dataproductversion_pb2_grpc
from github.com.metaprov.modelaapi.services.dataset.v1 import dataset_pb2_grpc
from github.com.metaprov.modelaapi.services.datasource.v1 import datasource_pb2_grpc
from github.com.metaprov.modelaapi.services.entity.v1 import entity_pb2_grpc
from github.com.metaprov.modelaapi.services.featurehistogram.v1 import featurehistogram_pb2_grpc
from github.com.metaprov.modelaapi.services.featurepipelinerun.v1 import featurepipelinerun_pb2_grpc
from github.com.metaprov.modelaapi.services.featurepipeline.v1 import featurepipeline_pb2_grpc
from github.com.metaprov.modelaapi.services.feature.v1 import feature_pb2_grpc
from github.com.metaprov.modelaapi.services.featureset.v1 import featureset_pb2_grpc
from github.com.metaprov.modelaapi.services.labelingpipelinerun.v1 import labelingpipelinerun_pb2_grpc
from github.com.metaprov.modelaapi.services.labelingpipeline.v1 import labelingpipeline_pb2_grpc
from github.com.metaprov.modelaapi.services.reciperun.v1 import reciperun_pb2_grpc
from github.com.metaprov.modelaapi.services.recipe.v1 import recipe_pb2_grpc
from github.com.metaprov.modelaapi.services.sqlquery.v1 import sqlquery_pb2_grpc
from github.com.metaprov.modelaapi.services.sqlqueryrun.v1 import sqlqueryrun_pb2_grpc
from github.com.metaprov.modelaapi.services.webrequestrun.v1 import webrequestrun_pb2_grpc
from github.com.metaprov.modelaapi.services.webrequest.v1 import webrequest_pb2_grpc
from github.com.metaprov.modelaapi.services.cronprediction.v1 import cronprediction_pb2_grpc
from github.com.metaprov.modelaapi.services.curtain.v1 import curtain_pb2_grpc
from github.com.metaprov.modelaapi.services.dataapp.v1 import dataapp_pb2_grpc
from github.com.metaprov.modelaapi.services.prediction.v1 import prediction_pb2_grpc
from github.com.metaprov.modelaapi.services.predictor.v1 import predictor_pb2_grpc
from github.com.metaprov.modelaapi.services.account.v1 import account_pb2_grpc
from github.com.metaprov.modelaapi.services.alert.v1 import alert_pb2_grpc
from github.com.metaprov.modelaapi.services.apitoken.v1 import apitoken_pb2_grpc
from github.com.metaprov.modelaapi.services.attachment.v1 import attachment_pb2_grpc
from github.com.metaprov.modelaapi.services.commit.v1 import commit_pb2_grpc
from github.com.metaprov.modelaapi.services.connection.v1 import connection_pb2_grpc
from github.com.metaprov.modelaapi.services.lab.v1 import lab_pb2_grpc
from github.com.metaprov.modelaapi.services.license.v1 import license_pb2_grpc
from github.com.metaprov.modelaapi.services.modelasystem.v1 import modelasystem_pb2_grpc
from github.com.metaprov.modelaapi.services.notifier.v1 import notifier_pb2_grpc
from github.com.metaprov.modelaapi.services.servingsite.v1 import servingsite_pb2_grpc
from github.com.metaprov.modelaapi.services.tenant.v1 import tenant_pb2_grpc
from github.com.metaprov.modelaapi.services.virtualbucket.v1 import virtualbucket_pb2_grpc
from github.com.metaprov.modelaapi.services.virtualcluster.v1 import virtualcluster_pb2_grpc
from github.com.metaprov.modelaapi.services.virtualvolume.v1 import virtualvolume_pb2_grpc
from github.com.metaprov.modelaapi.services.meeting.v1 import meeting_pb2_grpc
from github.com.metaprov.modelaapi.services.postmortem.v1 import postmortem_pb2_grpc
from github.com.metaprov.modelaapi.services.review.v1 import review_pb2_grpc
from github.com.metaprov.modelaapi.services.runbook.v1 import runbook_pb2_grpc
from github.com.metaprov.modelaapi.services.todo.v1 import todo_pb2_grpc
from github.com.metaprov.modelaapi.services.cronreport.v1 import cronreport_pb2_grpc
from github.com.metaprov.modelaapi.services.modelautobuilder.v1 import modelautobuilder_pb2_grpc
from github.com.metaprov.modelaapi.services.modelcompilerrun.v1 import modelcompilerrun_pb2_grpc
from github.com.metaprov.modelaapi.services.modelpipelinerun.v1 import modelpipelinerun_pb2_grpc
from github.com.metaprov.modelaapi.services.modelpipeline.v1 import modelpipeline_pb2_grpc
from github.com.metaprov.modelaapi.services.model.v1 import model_pb2_grpc
from github.com.metaprov.modelaapi.services.notebookrun.v1 import notebookrun_pb2_grpc
from github.com.metaprov.modelaapi.services.notebook.v1 import notebook_pb2_grpc
from github.com.metaprov.modelaapi.services.report.v1 import report_pb2_grpc
from github.com.metaprov.modelaapi.services.study.v1 import study_pb2_grpc

from modela.data.DataPipelineRun import *
from modela.data.DataPipeline import *
from modela.data.DataProduct import *
from modela.data.DataProductVersion import *
from modela.data.Dataset import *
from modela.data.DataSource import *
from modela.data.Entity import *
from modela.data.FeatureHistogram import *
from modela.data.FeaturePipelineRun import *
from modela.data.FeaturePipeline import *
from modela.data.Feature import *
from modela.data.Featureset import *
from modela.data.LabelingPipelineRun import *
from modela.data.LabelingPipeline import *
from modela.data.RecipeRun import *
from modela.data.Recipe import *
from modela.data.SqlQuery import *
from modela.data.SqlQueryRun import *
from modela.data.WebRequestRun import *
from modela.data.WebRequest import *
from modela.inference.CronPrediction import *
from modela.inference.Curtain import *
from modela.inference.DataApp import *
from modela.inference.Prediction import *
from modela.inference.Predictor import *
from modela.infra.Account import *
from modela.infra.Alert import *
from modela.infra.ApiToken import *
from modela.infra.Attachment import *
from modela.infra.Commit import *
from modela.infra.Connection import *
from modela.infra.Lab import *
from modela.infra.License import *
from modela.infra.ModelaSystem import *
from modela.infra.Notifier import *
from modela.infra.ServingSite import *
from modela.infra.Tenant import *
from modela.infra.VirtualBucket import *
from modela.infra.VirtualCluster import *
from modela.infra.VirtualVolume import *
from modela.team.Meeting import *
from modela.team.PostMortem import *
from modela.team.Review import *
from modela.team.RunBook import *
from modela.team.Todo import *
from modela.training.CronReport import *
from modela.training.ModelAutobuilder import *
from modela.training.ModelCompilerRun import *
from modela.training.ModelPipelineRun import *
from modela.training.ModelPipeline import *
from modela.training.Model import *
from modela.training.NotebookRun import *
from modela.training.Notebook import *
from modela.training.Report import *
from modela.training.Study import *


class Modela:
    def __init__(
        self,
        host="localhost",
        port=3000,
        interceptors: Optional[
            List[
                Union[
                    UnaryUnaryClientInterceptor,
                    UnaryStreamClientInterceptor,
                    StreamUnaryClientInterceptor,
                    StreamStreamClientInterceptor,
                ]
            ]
        ] = None,
    ):
        """Initializer.
           Creates a gRPC channel for connecting to the server.
           Adds the channel to the generated client stub.

        Arguments:
            None.

        Returns:
            None.
        """
        self._channel = grpc.insecure_channel('{0}:{1}'.format(host, port))

        if interceptors:
            self._channel = grpc.intercept_channel(  # type: ignore
                self._channel, *interceptors
            )

        self.__datapipelinerun_stub = datapipelinerun_pb2_grpc.DataPipelineRunServiceStub(self._channel)
        self.__datapipelinerun_client = DataPipelineRunClient(self.__datapipelinerun_stub)

        self.__datapipeline_stub = datapipeline_pb2_grpc.DataPipelineServiceStub(self._channel)
        self.__datapipeline_client = DataPipelineClient(self.__datapipeline_stub)

        self.__dataproduct_stub = dataproduct_pb2_grpc.DataProductServiceStub(self._channel)
        self.__dataproduct_client = DataProductClient(self.__dataproduct_stub)

        self.__dataproductversion_stub = dataproductversion_pb2_grpc.DataProductVersionServiceStub(self._channel)
        self.__dataproductversion_client = DataProductVersionClient(self.__dataproductversion_stub)

        self.__dataset_stub = dataset_pb2_grpc.DatasetServiceStub(self._channel)
        self.__dataset_client = DatasetClient(self.__dataset_stub)

        self.__datasource_stub = datasource_pb2_grpc.DataSourceServiceStub(self._channel)
        self.__datasource_client = DataSourceClient(self.__datasource_stub)

        self.__entity_stub = entity_pb2_grpc.EntityServiceStub(self._channel)
        self.__entity_client = EntityClient(self.__entity_stub)

        self.__featurehistogram_stub = featurehistogram_pb2_grpc.FeatureHistogramServiceStub(self._channel)
        self.__featurehistogram_client = FeatureHistogramClient(self.__featurehistogram_stub)

        self.__featurepipelinerun_stub = featurepipelinerun_pb2_grpc.FeaturePipelineRunServiceStub(self._channel)
        self.__featurepipelinerun_client = FeaturePipelineRunClient(self.__featurepipelinerun_stub)

        self.__featurepipeline_stub = featurepipeline_pb2_grpc.FeaturePipelineServiceStub(self._channel)
        self.__featurepipeline_client = FeaturePipelineClient(self.__featurepipeline_stub)

        self.__feature_stub = feature_pb2_grpc.FeatureServiceStub(self._channel)
        self.__feature_client = FeatureClient(self.__feature_stub)

        self.__featureset_stub = featureset_pb2_grpc.FeaturesetServiceStub(self._channel)
        self.__featureset_client = FeaturesetClient(self.__featureset_stub)

        self.__labelingpipelinerun_stub = labelingpipelinerun_pb2_grpc.LabelingPipelineRunServiceStub(self._channel)
        self.__labelingpipelinerun_client = LabelingPipelineRunClient(self.__labelingpipelinerun_stub)

        self.__labelingpipeline_stub = labelingpipeline_pb2_grpc.LabelingPipelineServiceStub(self._channel)
        self.__labelingpipeline_client = LabelingPipelineClient(self.__labelingpipeline_stub)

        self.__reciperun_stub = reciperun_pb2_grpc.RecipeRunServiceStub(self._channel)
        self.__reciperun_client = RecipeRunClient(self.__reciperun_stub)

        self.__recipe_stub = recipe_pb2_grpc.RecipeServiceStub(self._channel)
        self.__recipe_client = RecipeClient(self.__recipe_stub)

        self.__sqlquery_stub = sqlquery_pb2_grpc.SqlQueryServiceStub(self._channel)
        self.__sqlquery_client = SqlQueryClient(self.__sqlquery_stub)

        self.__sqlqueryrun_stub = sqlqueryrun_pb2_grpc.SqlQueryRunServiceStub(self._channel)
        self.__sqlqueryrun_client = SqlQueryRunClient(self.__sqlqueryrun_stub)

        self.__webrequestrun_stub = webrequestrun_pb2_grpc.WebRequestRunServiceStub(self._channel)
        self.__webrequestrun_client = WebRequestRunClient(self.__webrequestrun_stub)

        self.__webrequest_stub = webrequest_pb2_grpc.WebRequestServiceStub(self._channel)
        self.__webrequest_client = WebRequestClient(self.__webrequest_stub)

        self.__cronprediction_stub = cronprediction_pb2_grpc.CronPredictionServiceStub(self._channel)
        self.__cronprediction_client = CronPredictionClient(self.__cronprediction_stub)

        self.__curtain_stub = curtain_pb2_grpc.CurtainServiceStub(self._channel)
        self.__curtain_client = CurtainClient(self.__curtain_stub)

        self.__dataapp_stub = dataapp_pb2_grpc.DataAppServiceStub(self._channel)
        self.__dataapp_client = DataAppClient(self.__dataapp_stub)

        self.__prediction_stub = prediction_pb2_grpc.PredictionServiceStub(self._channel)
        self.__prediction_client = PredictionClient(self.__prediction_stub)

        self.__predictor_stub = predictor_pb2_grpc.PredictorServiceStub(self._channel)
        self.__predictor_client = PredictorClient(self.__predictor_stub)

        self.__account_stub = account_pb2_grpc.AccountServiceStub(self._channel)
        self.__account_client = AccountClient(self.__account_stub)

        self.__alert_stub = alert_pb2_grpc.AlertServiceStub(self._channel)
        self.__alert_client = AlertClient(self.__alert_stub)

        self.__apitoken_stub = apitoken_pb2_grpc.ApiTokenServiceStub(self._channel)
        self.__apitoken_client = ApiTokenClient(self.__apitoken_stub)

        self.__attachment_stub = attachment_pb2_grpc.AttachmentServiceStub(self._channel)
        self.__attachment_client = AttachmentClient(self.__attachment_stub)

        self.__commit_stub = commit_pb2_grpc.CommitServiceStub(self._channel)
        self.__commit_client = CommitClient(self.__commit_stub)

        self.__connection_stub = connection_pb2_grpc.ConnectionServiceStub(self._channel)
        self.__connection_client = ConnectionClient(self.__connection_stub)

        self.__lab_stub = lab_pb2_grpc.LabServiceStub(self._channel)
        self.__lab_client = LabClient(self.__lab_stub)

        self.__license_stub = license_pb2_grpc.LicenseServiceStub(self._channel)
        self.__license_client = LicenseClient(self.__license_stub)

        self.__modelasystem_stub = modelasystem_pb2_grpc.ModelaSystemServiceStub(self._channel)
        self.__modelasystem_client = ModelaSystemClient(self.__modelasystem_stub)

        self.__notifier_stub = notifier_pb2_grpc.NotifierServiceStub(self._channel)
        self.__notifier_client = NotifierClient(self.__notifier_stub)

        self.__servingsite_stub = servingsite_pb2_grpc.ServingSiteServiceStub(self._channel)
        self.__servingsite_client = ServingSiteClient(self.__servingsite_stub)

        self.__tenant_stub = tenant_pb2_grpc.TenantServiceStub(self._channel)
        self.__tenant_client = TenantClient(self.__tenant_stub)

        self.__virtualbucket_stub = virtualbucket_pb2_grpc.VirtualBucketServiceStub(self._channel)
        self.__virtualbucket_client = VirtualBucketClient(self.__virtualbucket_stub)

        self.__virtualcluster_stub = virtualcluster_pb2_grpc.VirtualClusterServiceStub(self._channel)
        self.__virtualcluster_client = VirtualClusterClient(self.__virtualcluster_stub)

        self.__virtualvolume_stub = virtualvolume_pb2_grpc.VirtualVolumeServiceStub(self._channel)
        self.__virtualvolume_client = VirtualVolumeClient(self.__virtualvolume_stub)

        self.__meeting_stub = meeting_pb2_grpc.MeetingServiceStub(self._channel)
        self.__meeting_client = MeetingClient(self.__meeting_stub)

        self.__postmortem_stub = postmortem_pb2_grpc.PostMortemServiceStub(self._channel)
        self.__postmortem_client = PostMortemClient(self.__postmortem_stub)

        self.__review_stub = review_pb2_grpc.ReviewServiceStub(self._channel)
        self.__review_client = ReviewClient(self.__review_stub)

        self.__runbook_stub = runbook_pb2_grpc.RunBookServiceStub(self._channel)
        self.__runbook_client = RunBookClient(self.__runbook_stub)

        self.__todo_stub = todo_pb2_grpc.TodoServiceStub(self._channel)
        self.__todo_client = TodoClient(self.__todo_stub)

        self.__cronreport_stub = cronreport_pb2_grpc.CronReportServiceStub(self._channel)
        self.__cronreport_client = CronReportClient(self.__cronreport_stub)

        self.__modelautobuilder_stub = modelautobuilder_pb2_grpc.ModelAutobuilderServiceStub(self._channel)
        self.__modelautobuilder_client = ModelAutobuilderClient(self.__modelautobuilder_stub)

        self.__modelcompilerrun_stub = modelcompilerrun_pb2_grpc.ModelCompilerRunServiceStub(self._channel)
        self.__modelcompilerrun_client = ModelCompilerRunClient(self.__modelcompilerrun_stub)

        self.__modelpipelinerun_stub = modelpipelinerun_pb2_grpc.ModelPipelineRunServiceStub(self._channel)
        self.__modelpipelinerun_client = ModelPipelineRunClient(self.__modelpipelinerun_stub)

        self.__modelpipeline_stub = modelpipeline_pb2_grpc.ModelPipelineServiceStub(self._channel)
        self.__modelpipeline_client = ModelPipelineClient(self.__modelpipeline_stub)

        self.__model_stub = model_pb2_grpc.ModelServiceStub(self._channel)
        self.__model_client = ModelClient(self.__model_stub)

        self.__notebookrun_stub = notebookrun_pb2_grpc.NotebookRunServiceStub(self._channel)
        self.__notebookrun_client = NotebookRunClient(self.__notebookrun_stub)

        self.__notebook_stub = notebook_pb2_grpc.NotebookServiceStub(self._channel)
        self.__notebook_client = NotebookClient(self.__notebook_stub)

        self.__report_stub = report_pb2_grpc.ReportServiceStub(self._channel)
        self.__report_client = ReportClient(self.__report_stub)

        self.__study_stub = study_pb2_grpc.StudyServiceStub(self._channel)
        self.__study_client = StudyClient(self.__study_stub)



    @property
    def Accounts(self):
        return self.__account_client

    def Account(self, namespace="", name="") -> Account:
        return Account(MDAccount(), self.Accounts, namespace=namespace, name=name)

    @property
    def DataProducts(self):
        return self.__dataproduct_client

    def DataProduct(self, namespace="", name="") -> DataProduct:
        return DataProduct(MDDataProduct(), self.DataProducts, namespace, name)

    @property
    def DataSources(self):
        return self.__datasource_client

    def DataSource(self, namespace="", name="") -> DataSource:
        return DataSource(MDDataSource(), self.DataSources, namespace, name)

    @property
    def DataPipelineRuns(self):
        return self.__datapipelinerun_client

    def DataPipelineRun(self, namespace="", name="") -> DataPipelineRun:
        return DataPipelineRun(MDDataPipelineRun(), self.DataPipelineRuns, namespace, name)

    @property
    def DataPipelines(self):
        return self.__datapipeline_client

    def DataPipeline(self, namespace="", name="") -> DataPipeline:
        return DataPipeline(MDDataPipeline(), self.DataPipelines, namespace, name)

    @property
    def DataProductVersions(self):
        return self.__dataproductversion_client

    def DataProductVersion(self, namespace="", name="") -> DataProductVersion:
        return DataProductVersion(MDDataProductVersion(), self.DataProductVersions, namespace, name)

    @property
    def Datasets(self):
        return self.__dataset_client

    def Dataset(self, namespace="", name="") -> Dataset:
        return Dataset(MDDataset(), self.Datasets, namespace, name)

    @property
    def Entitys(self):
        return self.__entity_client

    def Entity(self, namespace="", name="") -> Entity:
        return Entity(MDEntity(), self.Entitys, namespace, name)

    @property
    def FeatureHistograms(self):
        return self.__featurehistogram_client

    def FeatureHistogram(self, namespace="", name="") -> FeatureHistogram:
        return FeatureHistogram(MDFeatureHistogram(), self.FeatureHistograms, namespace, name)

    @property
    def FeaturePipelineRuns(self):
        return self.__featurepipelinerun_client

    def FeaturePipelineRun(self, namespace="", name="") -> FeaturePipelineRun:
        return FeaturePipelineRun(MDFeaturePipelineRun(), self.FeaturePipelineRuns, namespace, name)

    @property
    def FeaturePipelines(self):
        return self.__featurepipeline_client

    def FeaturePipeline(self, namespace="", name="") -> FeaturePipeline:
        return FeaturePipeline(MDFeaturePipeline(), self.FeaturePipelines, namespace, name)

    @property
    def Features(self):
        return self.__feature_client

    def Feature(self, namespace="", name="") -> Feature:
        return Feature(MDFeature(), self.Features, namespace, name)

    @property
    def Featuresets(self):
        return self.__featureset_client

    def Featureset(self, namespace="", name="") -> Featureset:
        return Featureset(MDFeatureset(), self.Featuresets, namespace, name)

    @property
    def LabelingPipelineRuns(self):
        return self.__labelingpipelinerun_client

    def LabelingPipelineRun(self, namespace="", name="") -> LabelingPipelineRun:
        return LabelingPipelineRun(MDLabelingPipelineRun(), self.LabelingPipelineRuns, namespace, name)

    @property
    def LabelingPipelines(self):
        return self.__labelingpipeline_client

    def LabelingPipeline(self, namespace="", name="") -> LabelingPipeline:
        return LabelingPipeline(MDLabelingPipeline(), self.LabelingPipelines, namespace, name)

    @property
    def RecipeRuns(self):
        return self.__reciperun_client

    def RecipeRun(self, namespace="", name="") -> RecipeRun:
        return RecipeRun(MDRecipeRun(), self.RecipeRuns, namespace, name)

    @property
    def Recipes(self):
        return self.__recipe_client

    def Recipe(self, namespace="", name="") -> Recipe:
        return Recipe(MDRecipe(), self.Recipes, namespace, name)

    @property
    def SqlQuerys(self):
        return self.__sqlquery_client

    def SqlQuery(self, namespace="", name="") -> SqlQuery:
        return SqlQuery(MDSqlQuery(), self.SqlQuerys, namespace, name)

    @property
    def SqlQueryRuns(self):
        return self.__sqlqueryrun_client

    def SqlQueryRun(self, namespace="", name="") -> SqlQueryRun:
        return SqlQueryRun(MDSqlQueryRun(), self.SqlQueryRuns, namespace, name)

    @property
    def WebRequestRuns(self):
        return self.__webrequestrun_client

    def WebRequestRun(self, namespace="", name="") -> WebRequestRun:
        return WebRequestRun(MDWebRequestRun(), self.WebRequestRuns, namespace, name)

    @property
    def WebRequests(self):
        return self.__webrequest_client

    def WebRequest(self, namespace="", name="") -> WebRequest:
        return WebRequest(MDWebRequest(), self.WebRequests, namespace, name)

    @property
    def CronPredictions(self):
        return self.__cronprediction_client

    def CronPrediction(self, namespace="", name="") -> CronPrediction:
        return CronPrediction(MDCronPrediction(), self.CronPredictions, namespace, name)

    @property
    def Curtains(self):
        return self.__curtain_client

    def Curtain(self, namespace="", name="") -> Curtain:
        return Curtain(MDCurtain(), self.Curtains, namespace, name)

    @property
    def DataApps(self):
        return self.__dataapp_client

    def DataApp(self, namespace="", name="") -> DataApp:
        return DataApp(MDDataApp(), self.DataApps, namespace, name)

    @property
    def Predictions(self):
        return self.__prediction_client

    def Prediction(self, namespace="", name="") -> Prediction:
        return Prediction(MDPrediction(), self.Predictions, namespace, name)

    @property
    def Predictors(self):
        return self.__predictor_client

    def Predictor(self, namespace="", name="") -> Predictor:
        return Predictor(MDPredictor(), self.Predictors, namespace, name)

    @property
    def Alerts(self):
        return self.__alert_client

    def Alert(self, namespace="", name="") -> Alert:
        return Alert(MDAlert(), self.Alerts, namespace, name)

    @property
    def ApiTokens(self):
        return self.__apitoken_client

    def ApiToken(self, namespace="", name="") -> ApiToken:
        return ApiToken(MDApiToken(), self.ApiTokens, namespace, name)

    @property
    def Attachments(self):
        return self.__attachment_client

    def Attachment(self, namespace="", name="") -> Attachment:
        return Attachment(MDAttachment(), self.Attachments, namespace, name)

    @property
    def Commits(self):
        return self.__commit_client

    def Commit(self, namespace="", name="") -> Commit:
        return Commit(MDCommit(), self.Commits, namespace, name)

    @property
    def Connections(self):
        return self.__connection_client

    def Connection(self, namespace="", name="") -> Connection:
        return Connection(MDConnection(), self.Connections, namespace, name)

    @property
    def Labs(self):
        return self.__lab_client

    def Lab(self, namespace="", name="") -> Lab:
        return Lab(MDLab(), self.Labs, namespace, name)

    @property
    def Licenses(self):
        return self.__license_client

    def License(self, namespace="", name="") -> License:
        return License(MDLicense(), self.Licenses, namespace, name)

    @property
    def ModelaSystems(self):
        return self.__modelasystem_client

    def ModelaSystem(self, namespace="", name="") -> ModelaSystem:
        return ModelaSystem(MDModelaSystem(), self.ModelaSystems, namespace, name)

    @property
    def Notifiers(self):
        return self.__notifier_client

    def Notifier(self, namespace="", name="") -> Notifier:
        return Notifier(MDNotifier(), self.Notifiers, namespace, name)

    @property
    def ServingSites(self):
        return self.__servingsite_client

    def ServingSite(self, namespace="", name="") -> ServingSite:
        return ServingSite(MDServingSite(), self.ServingSites, namespace, name)

    @property
    def Tenants(self):
        return self.__tenant_client

    def Tenant(self, namespace="", name="") -> Tenant:
        return Tenant(MDTenant(), self.Tenants, namespace, name)

    @property
    def VirtualBuckets(self):
        return self.__virtualbucket_client

    def VirtualBucket(self, namespace="", name="") -> VirtualBucket:
        return VirtualBucket(MDVirtualBucket(), self.VirtualBuckets, namespace, name)

    @property
    def VirtualClusters(self):
        return self.__virtualcluster_client

    def VirtualCluster(self, namespace="", name="") -> VirtualCluster:
        return VirtualCluster(MDVirtualCluster(), self.VirtualClusters, namespace, name)

    @property
    def VirtualVolumes(self):
        return self.__virtualvolume_client

    def VirtualVolume(self, namespace="", name="") -> VirtualVolume:
        return VirtualVolume(MDVirtualVolume(), self.VirtualVolumes, namespace, name)

    @property
    def Meetings(self):
        return self.__meeting_client

    def Meeting(self, namespace="", name="") -> Meeting:
        return Meeting(MDMeeting(), self.Meetings, namespace, name)

    @property
    def PostMortems(self):
        return self.__postmortem_client

    def PostMortem(self, namespace="", name="") -> PostMortem:
        return PostMortem(MDPostMortem(), self.PostMortems, namespace, name)

    @property
    def Reviews(self):
        return self.__review_client

    def Review(self, namespace="", name="") -> Review:
        return Review(MDReview(), self.Reviews, namespace, name)

    @property
    def RunBooks(self):
        return self.__runbook_client

    def RunBook(self, namespace="", name="") -> RunBook:
        return RunBook(MDRunBook(), self.RunBooks, namespace, name)

    @property
    def Todos(self):
        return self.__todo_client

    def Todo(self, namespace="", name="") -> Todo:
        return Todo(MDTodo(), self.Todos, namespace, name)

    @property
    def CronReports(self):
        return self.__cronreport_client

    def CronReport(self, namespace="", name="") -> CronReport:
        return CronReport(MDCronReport(), self.CronReports, namespace, name)

    @property
    def ModelAutobuilders(self):
        return self.__modelautobuilder_client

    def ModelAutobuilder(self, namespace="", name="") -> ModelAutobuilder:
        return ModelAutobuilder(MDModelAutobuilder(), self.ModelAutobuilders, namespace, name)

    @property
    def ModelCompilerRuns(self):
        return self.__modelcompilerrun_client

    def ModelCompilerRun(self, namespace="", name="") -> ModelCompilerRun:
        return ModelCompilerRun(MDModelCompilerRun(), self.ModelCompilerRuns, namespace, name)

    @property
    def ModelPipelineRuns(self):
        return self.__modelpipelinerun_client

    def ModelPipelineRun(self, namespace="", name="") -> ModelPipelineRun:
        return ModelPipelineRun(MDModelPipelineRun(), self.ModelPipelineRuns, namespace, name)

    @property
    def ModelPipelines(self):
        return self.__modelpipeline_client

    def ModelPipeline(self, namespace="", name="") -> ModelPipeline:
        return ModelPipeline(MDModelPipeline(), self.ModelPipelines, namespace, name)

    @property
    def Models(self):
        return self.__model_client

    def Model(self, namespace="", name="") -> Model:
        return Model(MDModel(), self.Models, namespace, name)

    @property
    def NotebookRuns(self):
        return self.__notebookrun_client

    def NotebookRun(self, namespace="", name="") -> NotebookRun:
        return NotebookRun(MDNotebookRun(), self.NotebookRuns, namespace, name)

    @property
    def Notebooks(self):
        return self.__notebook_client

    def Notebook(self, namespace="", name="") -> Notebook:
        return Notebook(MDNotebook(), self.Notebooks, namespace, name)

    @property
    def Reports(self):
        return self.__report_client

    def Report(self, namespace="", name="") -> Report:
        return Report(MDReport(), self.Reports, namespace, name)

    @property
    def Studies(self):
        return self.__study_client

    def Study(self, namespace="", name="") -> Study:
        return Study(MDStudy(), self.Studys, namespace, name)

    def close(self):
        if self._channel:
            self._channel.close()

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
