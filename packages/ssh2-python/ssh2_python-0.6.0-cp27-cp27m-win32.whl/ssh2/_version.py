
import json

version_json = '''
{"date": "2017-10-05T10:17:13.165000", "full-revisionid": "7080f34cb2c4d56f7ce60ab78b3939dc89a32320", "dirty": false, "version": "0.6.0", "error": null}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

