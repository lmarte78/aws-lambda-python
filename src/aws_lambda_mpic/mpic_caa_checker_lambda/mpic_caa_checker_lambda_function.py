from aws_lambda_powertools.utilities.parser import event_parser

from open_mpic_core.common_domain.check_request import CaaCheckRequest
from open_mpic_core.common_domain.remote_perspective import RemotePerspective
from open_mpic_core.mpic_caa_checker.mpic_caa_checker import MpicCaaChecker
import os


class MpicCaaCheckerLambdaHandler:
    def __init__(self):
        self.perspective = RemotePerspective(rir=os.environ['rir_region'], code=os.environ['AWS_REGION'])
        self.default_caa_domain_list = os.environ['default_caa_domains'].split("|")
        self.caa_checker = MpicCaaChecker(self.default_caa_domain_list, self.perspective)

    def process_invocation(self, caa_request: CaaCheckRequest):
        caa_response = self.caa_checker.check_caa(caa_request)
        result = {
            'statusCode': 200,  # note: must be snakeCase
            'headers': {'Content-Type': 'application/json'},
            'body': caa_response.model_dump_json()
        }
        return result


# Global instance for Lambda runtime
_handler = None


def get_handler() -> MpicCaaCheckerLambdaHandler:
    """
    Singleton pattern to avoid recreating the handler on every Lambda invocation
    """
    global _handler
    if _handler is None:
        _handler = MpicCaaCheckerLambdaHandler()
    return _handler


# noinspection PyUnusedLocal
# for now, we are not using context, but it is required by the lambda handler signature
@event_parser(model=CaaCheckRequest)
def lambda_handler(event: CaaCheckRequest, context):  # AWS Lambda entry point
    return get_handler().process_invocation(event)
