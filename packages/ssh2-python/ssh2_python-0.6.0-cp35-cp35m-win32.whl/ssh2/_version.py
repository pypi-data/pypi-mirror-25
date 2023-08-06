
import json

version_json = '''
{"dirty": false, "full-revisionid": "7080f34cb2c4d56f7ce60ab78b3939dc89a32320", "date": "2017-10-05T10:25:32.215665", "version": "0.6.0", "error": null}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

