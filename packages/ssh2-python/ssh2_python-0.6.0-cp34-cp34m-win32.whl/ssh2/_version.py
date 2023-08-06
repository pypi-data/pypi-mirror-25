
import json

version_json = '''
{"dirty": false, "error": null, "date": "2017-10-05T10:19:56.846163", "version": "0.6.0", "full-revisionid": "7080f34cb2c4d56f7ce60ab78b3939dc89a32320"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

