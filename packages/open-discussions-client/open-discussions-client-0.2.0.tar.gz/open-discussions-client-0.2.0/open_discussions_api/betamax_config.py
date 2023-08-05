"""Configuration for betamax"""
from betamax import Betamax
from betamax_serializers.pretty_json import PrettyJSONSerializer


def setup_betamax():
    """Do global configuration for betamax. This function is idempotent."""
    Betamax.register_serializer(PrettyJSONSerializer)

    config = Betamax.configure()
    config.cassette_library_dir = "cassettes"
    config.default_cassette_options['match_requests_on'] = ['uri', 'method']
    config.default_cassette_options['serialize_with'] = 'prettyjson'
