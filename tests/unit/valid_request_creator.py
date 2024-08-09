from aws_lambda_python.mpic_coordinator.domain.dcv_validation_method import DcvValidationMethod
from aws_lambda_python.mpic_coordinator.domain.dns_record_type import DnsRecordType


class ValidRequestCreator:
    @staticmethod
    def create_valid_caa_check_request():
        return {
            'api-version': '1.0.0',
            'system-params': {'identifier': 'test', 'perspective-count': 6, 'quorum': 4},
            'caa-details': {'certificate-type': 'tls-server'}
        }

    @staticmethod
    def create_valid_dcv_check_request(validation_method=DcvValidationMethod.DNS_GENERIC):
        validation_details = {}
        match validation_method:
            case DcvValidationMethod.DNS_GENERIC:
                validation_details = {'prefix': 'test', 'record-type': DnsRecordType.A, 'expected-challenge': 'test'}
            case DcvValidationMethod.HTTP_GENERIC:
                validation_details = {'path': 'http://example.com', 'expected-challenge': 'test'}  # noqa (not https)
            case DcvValidationMethod.TLS_USING_ALPN:
                validation_details = {'expected-challenge': 'test'}
        return {
            'api-version': '1.0.0',
            'system-params': {'identifier': 'test', 'perspective-count': 6, 'quorum': 4},
            'validation-method': validation_method,
            'validation-details': validation_details
        }