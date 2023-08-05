# -*- coding: utf-8 -*-

"""

About the library:
-----------------

This module provides the API message formats used in F-Interop.

The idea is to be able to have an
- organized and centralized way of dealing with the big amount of messages formats used in the platform;
- to be able to import (or just copy/paste) these messages formats from any component in the F-Interop platform,
- re-use this also for the integration testing;
- to have version control the messages e.g. messages_testcase_start API v1 and API v2;
- to have a direct way of exporting this as doc.


F-Interop conventions:
---------------------
- if event is a service request then the routing key (r_key) is control.someFunctionality.service
- a reply to a service will be on topic/r_key : control.someFunctionality.service.reply
- reply.correlation_id = request.correlation_id


Usage:
------
>>> from finterop.messages import *  # doctest: +SKIP
from finterop.msg import MsgTestCaseSkip
m = MsgTestCaseSkip()
>>> m
MsgTestCaseSkip(_api_version = 0.1.29, _type = testcoordination.testcase.skip, testcase_id = TD_COAP_CORE_02_v01, )
>>> m.routing_key
'control.testcoordination'
>>> m.message_id # doctest: +SKIP
'802012eb-24e3-45c4-9dcc-dc293c584f63'
>>> m.testcase_id
'TD_COAP_CORE_02_v01'

# also we can modify some of the fields (rewrite the default ones)
>>> m = MsgTestCaseSkip(testcase_id = 'TD_COAP_CORE_03_v01')
>>> m
MsgTestCaseSkip(_api_version = 0.1.29, _type = testcoordination.testcase.skip, testcase_id = TD_COAP_CORE_03_v01, )
>>> m.testcase_id
'TD_COAP_CORE_03_v01'

# and even export the message in json format (for example for sending the message though the amqp event bus)
>>> m.to_json()
'{"_api_version": "0.1.29", "_type": "testcoordination.testcase.skip", "testcase_id": "TD_COAP_CORE_03_v01"}'

# We can use the Message class to import json into Message objects:
>>> m=MsgTestSuiteStart()
>>> m.to_json()
'{"_api_version": "0.1.29", "_type": "testcoordination.testsuite.start"}'
>>> json_message = m.to_json()
>>> obj=Message.from_json(json_message)
>>> type(obj)
<class 'messages.MsgTestSuiteStart'>

# We can use the library for generating error responses:
# the request:
>>> m = MsgSniffingStart()
>>>
# the error reply (note that we pass the message of the request to build the reply):
>>> err = MsgErrorReply(m)
>>> err
MsgErrorReply(_api_version = 0.1.29, _type = sniffing.start, error_code = Some error code TBD, error_message = Some error message TBD, ok = False, )
>>> m.reply_to
'control.sniffing.service.reply'
>>> err.routing_key
'control.sniffing.service.reply'

>>> m.correlation_id # doctest: +SKIP
'360b0f67-4455-43e3-a00f-eca91f2e84da'
>>> err.correlation_id # doctest: +SKIP
'360b0f67-4455-43e3-a00f-eca91f2e84da'

"""

import json
import time
import uuid
from collections import OrderedDict

#
# from finterop.msg.agent import (
#     MsgAgentTunStart,
#     MsgAgentTunStarted
# )
# from finterop.msg.dissection import (
#     MsgDissectionDissectCapture,
#     MsgDissectionDissectCaptureReply,
#     MsgDissectionAutoDissect
# )
# from finterop.msg.sniffing import (
#     MsgSniffingStart,
#     MsgSniffingStop,
#     MsgSniffingGetCapture,
#     MsgSniffingGetCaptureLast
# )
# from finterop.msg.tests import (
#     MsgTestSuiteStart,
#     MsgTestSuiteFinish,
#     MsgTestCaseReady,
#     MsgTestCaseStart,
#     MsgTestCaseConfiguration,
#     MsgTestCaseStop,
#     MsgTestCaseRestart,
#     MsgStepExecute,
#     MsgStimuliExecuted,
#     MsgCheckResponse,
#     MsgVerifyResponse,
#     MsgTestCaseFinish,
#     MsgTestCaseFinished,
#     MsgTestCaseSkip,
#     MsgTestCaseSelect,
#     MsgTestSuiteAbort,
#     MsgTestSuiteGetStatus,
#     MsgTestSuiteGetStatusReply,
#     MsgTestSuiteGetTestCases,
#     MsgTestSuiteGetTestCasesReply,
#     MsgTestCaseVerdict,
#     MsgTestSuiteReport
# )
#
# from schemas.finterop.msg.session import (
#     MsgInteropSessionConfiguration,
#     MsgTestingToolConfigured,
#     MsgTestingToolComponentReady,
#     MsgTestingToolComponentShutdown,
#     MsgTestingToolReady,
#     MsgTestingToolTerminate
# )
#
# message_types_dict = {
#     "tun.start": MsgAgentTunStart,  # TestingTool -> Agent
#     "tun.started": MsgAgentTunStarted,  # Agent -> TestingTool
#     "session.interop.configuration": MsgInteropSessionConfiguration,  # Orchestrator -> TestingTool
#     "testingtool.configured": MsgTestingToolConfigured,  # TestingTool -> Orchestrator, GUI
#     "testingtool.component.ready": MsgTestingToolComponentReady,  # Testing Tool internal
#     "testingtool.component.shutdown": MsgTestingToolComponentShutdown,  # Testing Tool internal
#     "testingtool.ready": MsgTestingToolReady,  # GUI Testing Tool -> GUI
#     "testingtool.terminate": MsgTestingToolTerminate,  # orchestrator -> TestingTool
#     "testcoordination.testsuite.start": MsgTestSuiteStart,  # GUI -> TestingTool
#     "testcoordination.testsuite.finish": MsgTestSuiteFinish,  # GUI -> TestingTool
#     "testcoordination.testcase.ready": MsgTestCaseReady,  # TestingTool -> GUI
#     "testcoordination.testcase.start": MsgTestCaseStart,  # GUI -> TestingTool
#     "testcoordination.step.execute": MsgStepExecute,  # TestingTool -> GUI
#     "testcoordination.testcase.configuration": MsgTestCaseConfiguration,  # TestingTool -> GUI
#     "testcoordination.testcase.stop": MsgTestCaseStop,  # GUI -> TestingTool
#     "testcoordination.testcase.restart": MsgTestCaseRestart,  # GUI -> TestingTool
#     "testcoordination.step.stimuli.executed": MsgStimuliExecuted,  # GUI -> TestingTool
#     "testcoordination.step.check.response": MsgCheckResponse,  # GUI -> TestingTool
#     "testcoordination.step.verify.response": MsgVerifyResponse,  # GUI -> TestingTool
#     "testcoordination.testcase.skip": MsgTestCaseSkip,  # GUI -> TestingTool
#     "testcoordination.testcase.select": MsgTestCaseSelect,  # GUI -> TestingTool
#     "testcoordination.testcase.finish": MsgTestCaseFinish,  # GUI -> TestingTool
#     "testcoordination.testcase.finished": MsgTestCaseFinished,  # TestingTool -> GUI
#     "testcoordination.testcase.verdict": MsgTestCaseVerdict,  # TestingTool -> GUI
#     "testcoordination.testsuite.abort": MsgTestSuiteAbort,  # GUI -> TestingTool
#     "testcoordination.testsuite.getstatus": MsgTestSuiteGetStatus,  # GUI -> TestingTool
#     "testcoordination.testsuite.getstatus.reply": MsgTestSuiteGetStatusReply,  # TestingTool -> GUI (reply)
#     "testcoordination.testsuite.gettestcases": MsgTestSuiteGetTestCases,  # GUI -> TestingTool
#     "testcoordination.testsuite.gettestcases.reply": MsgTestSuiteGetTestCasesReply,  # TestingTool -> GUI (reply)
#     "testcoordination.testsuite.report": MsgTestSuiteReport,  # TestingTool -> GUI
#     "sniffing.start": MsgSniffingStart,  # Testing Tool Internal
#     "sniffing.stop": MsgSniffingStop,  # Testing Tool Internal
#     "sniffing.getcapture": MsgSniffingGetCapture,  # Testing Tool Internal
#     "sniffing.getlastcapture": MsgSniffingGetCaptureLast,  # Testing Tool Internal
#     "dissection.dissectcapture": MsgDissectionDissectCapture,  # Testing Tool Internal
#     "dissection.dissectcapture.reply": MsgDissectionDissectCaptureReply,  # Testing Tool Internal
#     "dissection.autotriggered": MsgDissectionAutoDissect,  # TestingTool -> GUI
#     # GUI (or Orchestrator?) -> TestingTool
# }
#

from cerberus import Validator


class NonCompliantMessageFormatError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Message:
    def __init__(self, **kwargs):
        version = '0.1.30'

        # hard copy the message template
        self._msg_data = {k: v for k, v in self._msg_data_template.items()}

        # init properties
        self._properties = dict(
            content_type="application/json",
            message_id=str(uuid.uuid4()),
            timestamp=int(time.time())
        )

        try:
            if self.routing_key.endswith(".service"):
                self._properties["reply_to"] = "%s.%s" % (self.routing_key, "reply")
                self._properties["correlation_id"] = self._properties["message_id"]
        except AttributeError:
            pass

        # rewrite default data fields with the passed args
        self._msg_data.update(kwargs)

        # add API's version
        self._msg_data["_api_version"] = version

        # add values as objects attributes
        for key in self._msg_data:
            setattr(self, key, self._msg_data[key])

        # add props as objects attributes
        for key in self._properties:
            setattr(self, key, self._properties[key])

    def to_dict(self):
        resp = {}
        # let's use sorted so API returns items inside always in the same order
        for field in sorted(self._msg_data.keys()):
            resp[field] = getattr(self, field)

        return OrderedDict(sorted(resp.items(), key=lambda t: t[0]))  # sorted by key

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True)

    def get_properties(self):
        resp = OrderedDict()
        for field in self._properties:
            resp[field] = getattr(self, field)
        return resp

    def validate(self):
        pass

    def __str__(self):
        s = " - " * 20 + "\n"
        s += "Message routing key: %s" % self.routing_key
        s += "\n -  -  - \n"
        s += "Message properties: %s" % json.dumps(self.get_properties(), indent=4, )
        s += "\n -  -  - \n"
        s += "Message body: %s" % json.dumps(self.to_dict(), indent=4, )
        s += "\n" + " - " * 20
        return s

    def update_properties(self, **kwargs):
        for key, value in kwargs.items():
            if key in self._properties:
                setattr(self, key, value)

    @classmethod
    def from_json(cls, body):
        """
        :param body: json string or string encoded as utf-8
        :return:  Message object generated from the body
        :raises NonCompliantMessageFormatError: If the message cannot be build from the provided json
        """

        if type(body) is str:
            message_dict = json.loads(body)
        # Note: pika re-encodes json.dumps strings as utf-8 for some reason, the following line undoes this
        elif type(body) is bytes:
            message_dict = json.loads(body.decode("utf-8"))
        else:
            raise NonCompliantMessageFormatError("Not a Json")

        # check fist if it's a response
        if "ok" in message_dict:
            # cannot build a complete reply message just from the json representation
            return

        return cls.from_dict(message_dict)

    @classmethod
    def from_dict(cls, message_dict):
        """
        :param message_dict:
        :return:  Message object generated from the body
        :raises NonCompliantMessageFormatError: If the message cannot be build from the provided json
        """
        assert type(message_dict) is dict

        # check fist if it's a response
        if "ok" in message_dict:
            # cannot build a complete reply message just from the json representation
            return

        message_type = message_dict["_type"]

        # if message_type in message_types_dict:
        #     return message_types_dict[message_type](**message_dict)
        # else:
        #     raise NonCompliantMessageFormatError("Cannot load json message: %s" % str(message_dict))

    def __repr__(self):
        ret = "%s(" % self.__class__.__name__
        for key, value in self.to_dict().items():
            ret += "%s = %s, " % (key, value)
        ret += ")"
        return ret


class MsgReply(Message):
    """
    Auxiliary class which creates replies messages with fields based on the request.
    Routing key, corr_id and _type are generated based on the request message
    """

    def __init__(self, request_message, **kwargs):
        assert request_message

        self.routing_key = request_message.routing_key + ".reply"

        # if not data template, then let's build one for a reply
        # (possible when creating a MsgReply directly and not by using subclass)
        if not hasattr(self, "_msg_data_template"):
            self._msg_data_template = {
                "_type": request_message._type,
                "ok": True,
            }

        super(MsgReply, self).__init__(**kwargs)

        # overwrite correlation id template and attribute
        self._properties["correlation_id"] = request_message.correlation_id
        self.correlation_id = request_message.correlation_id


class MsgErrorReply(MsgReply):
    """
    see section "F-Interop conventions" on top
    """

    def __init__(self, request_message, **kwargs):
        assert request_message
        # msg_data_template doesnt include _type cause this class is generic, we can only get this at init from request
        # so, let's copy the _type from request and let the MsgReply handle the rest of the fields
        self._msg_data_template["_type"] = request_message._type
        super(MsgErrorReply, self).__init__(request_message, **kwargs)

    _msg_data_template = {
        "ok": False,
        "error_message": "Some error message TBD",
        "error_code": "Some error code TBD"
    }


class MsgTestSuiteStart(Message):
    """
    Requirements: Testing Tool MUST listen to event
    Type: Event
    Typical_use: GUI -> Testing Tool
    Description: tbd
    """

    routing_key = "control.testsuite.start"

    _msg_data_template = {
        "_type": "testcoordination.testsuite.start",
    }


class MsgTestSuiteFinish(Message):
    """
    Requirements: Testing Tool MUST listen to event
    Type: Event
    Typical_use: GUI -> Testing Tool
    Description: tbd
    """

    routing_key = "control.testsuite.finish"

    _msg_data_template = {
        "_type": "testcoordination.testsuite.finish",
    }


class MsgTestCaseReady(Message):
    """
    Requirements: Testing Tool MUST publish event
    Type: Event
    Typical_use: GUI -> Testing Tool
    Description:
        - Used to indicate to the GUI (or automated-iut) which is the next test case to be executed.
        - This message is normally followed by a MsgTestCaseStart (from GUI-> Testing Tool)
    """

    routing_key = "control.testcase.ready"

    _msg_data_template = {
        "_type": "testcoordination.testcase.ready",
        "message": "TBD",
        "testcase_id": "TBD",
        "testcase_ref": "TBD",
        "objective": "TBD",
        "state": None
    }


class MsgTestCaseStart(Message):
    """
    Requirements: Testing Tool MUST listen to event
    Type: Event
    Typical_use: GUI -> Testing Tool
    Description:
        - Message used for indicating the testing tool to start the test case (the one previously selected)
    """
    routing_key = "control.testcase.start"

    _msg_data_template = {
        "_type": "testcoordination.testcase.start",
    }


class MsgTestCaseConfiguration(Message):
    """
    Requirements: Testing Tool MAY publish event (if needed for executing the test case)
    Type: Event
    Typical_use: Testing Tool -> GUI & automated-iut
    Description:
        - Message used to indicate GUI and/or automated-iut which configuration to use.
    """
    routing_key = "control.testcase.configuration"

    _msg_data_template = {
        "_type": "testcoordination.testcase.configuration",
        "configuration_id": "COAP_CFG_01_v01",
        "node": "coap_server",
        "testcase_id": "TBD",
        "testcase_ref": "TBD",
        "message": ""
    }


class MsgTestCaseStop(Message):
    """
    Requirements: Testing Tool MUST listen to event
    Type: Event
    Typical_use: GUI & automated-iut -> Testing Tool
    Description:
        - Message used for indicating the testing tool to stop the test case (the one running).
    """

    routing_key = "control.testcase.stop"

    _msg_data_template = {
        "_type": "testcoordination.testcase.stop",
    }


class MsgTestCaseRestart(Message):
    """
    Requirements: Testing Tool MUST listen to event
    Type: Event
    Typical_use: GUI -> Testing Tool
    Description: Restart the running test cases.
    """

    routing_key = "control.testcase.restart"

    _msg_data_template = {
        "_type": "testcoordination.testcase.restart",
    }


class MsgStepFail(Message):
    routing_key = "control.step.fail"
    _msg_data_template = {
        "_type": "testcoordination.teststep.fail",
    }


class MsgStepExecute(Message):
    """
    Requirements: Testing Tool MUST publish event
    Type: Event
    Typical_use: Testing Tool -> GUI
    Description:
        - Used to indicate to the GUI (or automated-iut) which is the step to be executed by the user (or automated-IUT).
    """

    routing_key = "control.step.execute"

    _msg_data_template = {
        "_type": "testcoordination.step.execute",
        "message": "TBD",
        "step_id": "TBD",
        "step_type": "TBD",
        "step_info": [],
        "step_state": "executing",
        "node_execution_mode": "user_assisted",
        "testcase_id": "TBD",
        "testcase_ref": "TBD"
    }


class MsgStimuliExecuted(Message):
    """
    Requirements: Testing Tool MUST listen to event
    Type: Event
    Typical_use: GUI (or automated-IUT)-> Testing Tool
    Description:
        - Used to indicate stimuli has been executed by user (and it's user-assisted iut) or by automated-iut
    """

    routing_key = "control.step.executed"

    _msg_data_template = {
        "_type": "testcoordination.step.stimuli.executed",
    }


class MsgCheckResponse(Message):
    """
    Requirements: Testing Tool SHOULD implement (other components should not subscribe to event)
    Type: Event
    Typical_use: test coordination -> test analysis
    Description:
        - In the context of IUT to IUT test execution, this message is used for indicating that the previously executed
        messages (stimuli message and its reply) CHECK or comply to what is described in the Test Description.
        - Not used in CoAP testing Tool (analysis of traces is done post mortem)
    """

    routing_key = "control.step.check.response"

    _msg_data_template = {
        "_type": "testcoordination.step.check.response",
        "partial_verdict": "pass",
        "description": "TAT says: step complies (checks) with specification"
    }


class MsgVerifyResponse(Message):
    """
    Requirements: Testing Tool MUST listen to event
    Type: Event
    Typical_use: GUI (or automated-IUT)-> Testing Tool
    Description:
        - Message provided by user declaring if the IUT VERIFY the step previously executed as described in the Test
        Description.
    """

    routing_key = "control.step.verify.response"

    _msg_data_template = {
        "_type": "testcoordination.step.verify.response",
        "verify_response": True,
        "response_type": "bool"
    }


class MsgTestCaseFinish(Message):
    """
    TODO: TBD if needed or not

    Requirements: Testing Tool MAY listen to event
    Type: Event
    Typical_use: GUI (or automated-IUT)-> Testing Tool
    Description:
        - Used for indicating that the test case has finished.
        - Test coordinator deduces it automatically by using the testcase's step sequence
        - Not used in CoAP Testing Tool.
    """

    routing_key = "control.testcase.finish"

    _msg_data_template = {
        "_type": "testcoordination.testcase.finish",
    }


class MsgTestCaseFinished(Message):
    """
    Requirements: Testing Tool MUST publish event
    Type: Event
    Typical_use: Testing Tool -> GUI
    Description:
        - Used for indicating to subscribers that the test cases has finished.
        - This message is followed by a verdict.
    """

    routing_key = "control.testcase.finished"

    _msg_data_template = {
        "_type": "testcoordination.testcase.finished",
        "testcase_id": "",
        "testcase_ref": "",
        "message": "Testcase finished"
    }


class MsgTestSuiteAbort(Message):
    """
    Requirements: Testing Tool MUST listen to event
    Type: Event
    Typical_use: GUI (or automated-IUT)-> Testing Tool
    Description: tbd
    """

    routing_key = "control.testsuite.abort"

    _msg_data_template = {
        "_type": "testcoordination.testsuite.abort",
    }


class MsgTestSuiteGetStatus(Message):
    """
    Requirements: Testing Tool SHOULD implement (other components should not subscribe to event)
    Type: Request (service)
    Typical_use: GUI -> Testing Tool
    Description:
        - Describes current state of the test suite.
        - Format for the response not standardised.
    """

    routing_key = "control.testsuite.getstatus"

    _msg_data_template = {
        "_type": "testcoordination.testsuite.getstatus",
    }


class MsgTestSuiteGetStatusReply(MsgReply):
    """
    Requirements: Testing Tool SHOULD implement (other components should not subscribe to event)
    Type: Reply (service)
    Typical_use: Testing Tool -> GUI
    Description:
        - Describes current state of the test suite.
        - Format for the response not standardised.
    """

    routing_key = "control.testsuite.getstatus.reply"

    _msg_data_template = {
        "_type": "testcoordination.testsuite.getstatus.reply",
        "ok": True,
        "started": True,
        "testcase_id": "",
        "testcase_state": "executing",
        "step_id": ""

    }


class MsgTestCaseVerdict(Message):
    """
    Requirements: Testing Tool MUST publish event
    Type: Event
    Typical_use: Testing Tool -> GUI
    Description: Used to indicate to the GUI (or automated-iut) which is the final verdict of the testcase.
    """

    routing_key = "control.testcase.verdict"

    _msg_data_template = {
        "_type": "testcoordination.testcase.verdict",
        "verdict": "pass",
        "description": "No interoperability error was detected,",
        "partial_verdicts": [],
        "testcase_id": "",
        "testcase_ref": "",
        "objective": "Perform GET transaction(CON mode)",
        "state": "finished"
    }


class MsgTestSuiteReport(Message):
    """
    Requirements: Testing Tool MUST publish event
    Type: Event
    Typical_use: Testing Tool -> GUI
    Description: Used to indicate to the GUI (or automated-iut) the final results of the test session.
    """

    routing_key = "control.testsuite.report"

    _msg_data_template = {
        "_type": "testcoordination.testsuite.report",
        "TD_6TiSCH_6P_01_v01": {
            "verdict": "pass",
            "description": "No interoperability error was detected,",
            "partial_verdicts": []
        },

        "TD_6TiSCH_6P_02_v01": {
            "verdict": "pass",
            "description": "No interoperability error was detected,",
            "partial_verdicts": []
        }
    }


class MsgStepSuccess(Message):
    routing_key = "control.test.step.success"

    _msg_data_template = {}


class MsgPcapng(Message):
    routing_key = "data.pcapng"

    _msg_data_template = {}


class MsgAgentJSON(Message):
    routing_key = "sniffer.data"

    _msg_data_template = {}


class MsgFlashSniffer(Message):
    routing_key = "control.flash.sniffer"

    _msg_data_template = {}


class MsgSnifferStart(Message):
    routing_key = "control.sniffer.start"

    _msg_data_template = {}


class MsgOpenvisualizerSnifferStart(Message):
    routing_key = "control.sniffer_openvisualizer.start"

    _msg_data_template = {}


class MsgSnifferChannel(Message):
    routing_key = "control.sniffer.channel"

    _msg_data_template = {}


class MsgDisplayFilter(Message):
    routing_key = "control.sniffer.display_filter"

    _msg_data_template = {}


class MsgTestingToolTerminate(Message):
    """
    Requirements: Testing Tool MUST listen to event
    Type: Event
    Typical_use: GUI, (or Orchestrator) -> Testing Tool
    Description: Testing tool should stop all it's processes gracefully.
    """
    routing_key = "control.session.terminate"

    _msg_data_template = {
        "_type": "testingtool.terminate",
    }


class MsgTestingToolReady(Message):
    """
    Requirements: Testing Tool MUST publish event
    Type: Event
    Typcal_use: Testing Tool -> GUI
    Description: Used to indicate to the GUI that testing is ready to start the test suite
    """
    routing_key = "control.session.ready"

    _msg_data_template = {}


class MsgInteropSessionConfiguration(Message):
    """
    Requirements: Testing Tool MUST listen to event
    Type: Event
    Typical_use: Orchestrator -> Testing Tool
    Description: Testing tool MUST listen to this message and configure the testsuite correspondingly
    """
    routing_key = "session.interop.configuration"

    _msg_data_template = {
        "_type": "session.interop.configuration",
        "session_id": "TBD",
        "testing_tools": "f-interop/interoperability-6tisch",
        "users": [],
        "iuts": [],
        "tests": []
    }


class MsgTestingToolConfigured(Message):
    """
    Requirements: Testing Tool MUST publish event
    Type: Event
    Typical_use: Testing Tool -> Orchestrator, GUI
    Description: The goal is to notify orchestrator and other components that the testing tool has been configured
    """

    routing_key = "control.session.configured"
    _msg_data_template = {}


class MsgDissection(Message):
    routing_key = "dissected_frame"


class MsgContext(Message):
    routing_key = "config.context"

    _msg_data_template = {}


class MsgManagerStatsReq(Message):
    routing_key = "control.manager.req.stats"

    _msg_data_template = {}


class MsgManagerStatsRep(Message):
    routing_key = "control.manager.rep.stats"

    _msg_data_template = {}


class MsgAgentConfig(Message):
    routing_key = "control.agent.config"

    _msg_data_template = {}


class MsgAgentSolicitation(Message):
    routing_key = "control.agent.solicitation"
    _msg_data_template = {}


class MsgAgentTunStart(Message):
    """
    Requirements: Testing Tool MAY implement (if IP tun needed)
    Type: Event
    Typical_use: Testing Tool -> Agent
    Description: Message for triggering start IP tun interface in OS where the agent is running
    """
    routing_key = "control.agent.tun.start"

    _msg_data_template = {
        "_type": "tun.start",
        "name": "agent_TT",
        "ipv6_prefix": "bbbb",
        "ipv6_host": ":3",
        "ipv6_no_forwarding": False,
        "ipv4_host": None,
        "ipv4_network": None,
        "ipv4_netmask": None,
    }


class MsgAgentTunStarted(Message):
    """
    Description: Message for indicating that agent tun has been started
    Type: Event
    Typical_use: Testing Tool -> Agent
    Description: TBD
    """
    routing_key = "control.agent.tun.started"

    _msg_data_template = {
        "_type": "tun.started",
        "name": "agent_TT",
        "ipv6_prefix": "bbbb",
        "ipv6_host": ":3",
        "ipv4_host": None,
        "ipv4_network": None,
        "ipv4_netmask": None,
        "ipv6_no_forwarding": False,
    }


class MsgAgentPingRequest(Message):
    routing_key = "control.agent.ping"

    _msg_data_template = {}


class MsgOpenvisualizerNotification(Message):
    routing_key = "data.agent.openvisualizer"

    _msg_data_template = {}


agent_pcap_validator = Validator(
    {
        "_type": {
            "type": "string"
        },
        "value": {
            "type": "string"
        },
        "file_enc": {
            "type": "string"
        }
    },
    allow_unknown=True)
