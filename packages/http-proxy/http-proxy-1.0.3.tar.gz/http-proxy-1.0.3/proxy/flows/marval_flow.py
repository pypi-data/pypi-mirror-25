import os
import random

import suds.sudsobject
from proxy.parser.http_parser import HttpResponse
from proxy.pipe.recipe.flow import Flow
from proxy.pipe.recipe.matchers import has_path_starting
from proxy.pipe.recipe.soap import SoapFlow, default_response


def register_flow(flow: Flow):
    service = NarwhalsService()
    flow.delegate(service.flow)
    flow.when(has_path_starting("/MSM/RFP/Forms/Request.aspx")).respond(service.show_request)
    return flow


realpath = os.path.realpath(__file__)
dir = os.path.dirname(realpath)
url = 'file://' + dir + "/Marval.wsdl"
client = suds.client.Client(url)

VALUES = {
    "customer": {
        "Dusan Jakub": 990077,
        "MarvalCustomer1": 990066,
        "Notes Author1": 990055
    },
    "Assignee": {
        "my assignee1": 10001
    },
    "Impact": {
        "impact1": 20001
    },
    "RequestType": {
        "INC": 30001
    },
    "Priority": {
        "priority1": 40001
    },
    "ProjectCode": {
        "project1": 50001
    },
    "Service": {
        "service1": 60001,
        "subservice1": 60001
    },
    "Status": {
        "status_new": 70001,
        "status_reopened": 70002,
        "status_closed": 70003
    },
    "Tracker": {
        "my tracker1": 80001
    },
    "Urgency": {
        "urgency1": 90001
    },
    "Workflow": {
        "Default Workflow1": 11001
    },
    "Classification": {
        "classification_create1": 12001,
        "classification_create2": 12002,
        "classification_close1": 12003,
        "classification_close2": 12004
    }
}


class NarwhalsService:
    flow = SoapFlow(client, "/MSMWebService/WebService.asmx", on_mismatch=SoapFlow.DUMMY_RESPONSE)

    def __init__(self):
        self.tickets = {}

    @flow.respond_soap(flow.factory.Login())
    def handle_Login(self, request):
        if request.username != "marval" and request.password != "marval":
            raise "Invalid login"

        return self.flow.factory.LoginResponse(
            LoginResult=r"session123"
        )

    @flow.respond_soap(flow.factory.Logout(
        sessionKey=r"session123"
    )
    )
    def handle_Logout(self, request):
        return self.flow.factory.LogoutResponse()

    @flow.respond_soap(flow.factory.GetFirstCustomerIdByName())
    def handle_GetFirstCustomerIdByName(self, request):
        id = VALUES["customer"].get(request.nameString, None)
        if not id:
            raise Exception("Invalid customer")

        return self.flow.factory.GetFirstCustomerIdByNameResponse(
            GetFirstCustomerIdByNameResult=id
        )

    @flow.respond_soap(flow.factory.GetSystemIdFromName())
    def handle_GetSystemIdFromName(self, request):
        table = VALUES.get(request.entityType, None)
        if not table:
            raise Exception("Invalid/Unknown entity type " + request.entityType)

        id = table.get(request.entityName, None)
        if not table:
            raise Exception("Invalid/Unknown entity type " + request.entityType)

        return self.flow.factory.GetSystemIdFromNameResponse(
            GetSystemIdFromNameResult=id
        )

    @flow.respond_soap(flow.factory.GetConfigurationItemIdByNumber())
    def handle_GetConfigurationItemIdByNumber(self, request):
        "For simplicity, always return the same id with 00 appended"
        return self.flow.factory.GetConfigurationItemIdByNumberResponse(
            GetConfigurationItemIdByNumberResult=int(request.assetNo) * 100
        )

    @flow.respond_soap(flow.factory.GetFullRequestNumberByRequestId())
    def handle_GetFullRequestNumberByRequestId(self, request):
        return self.flow.factory.GetFullRequestNumberByRequestIdResponse(
            GetFullRequestNumberByRequestIdResult="MarvalTicket #" + str(request.requestId)
        )

    @flow.respond_soap(flow.factory.RaiseRequest())
    def handle_RaiseRequest(self, request):
        id = random.randrange(1000000)
        request.request.Identifier = id
        self.tickets[id] = request.request
        return self.flow.factory.RaiseRequestResponse(
            RaiseRequestResult=id
        )

    @flow.respond_soap(flow.factory.ViewRequest())
    def handle_ViewRequest(self, request):
        return self.flow.factory.ViewRequestResponse(
            ViewRequestResult=self.tickets[request.requestId]
        )

    @flow.respond_soap(flow.factory.UpdateRequest())
    def handle_UpdateRequest(self, request):
        self.tickets[request.request.Identifier] = request.request
        return self.flow.factory.UpdateRequestResponse(
            UpdateRequestResult=self.tickets[request.request.Identifier]
        )

    def show_request(self, request):
        id = request.path_query.get(b"id", None)
        if not id:
            return HttpResponse(b"400", b"Bad request", "Missing parameter id")

        ticket = self.tickets.get(int(id), None)
        if not ticket:
            return HttpResponse(b"404", b"Not found", "Request with id {} not found".format(id).encode())

        return HttpResponse.ok(ticket)
