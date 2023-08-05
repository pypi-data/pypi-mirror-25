import json
import yaml

def getJson():
	try:
		f = open("repository.yaml", "r")
		response = f.read()
		original = yaml.load(response)
		data = json.loads(json.dumps(original))
		return data
	except:
		return None

def massage(journey_metric, event):
	try:
		event['config'] = {}
		event['config']['repository_id'] = journey_metric['id'] if journey_metric.get("id") else ''
		event['config']['target_runtimes'] = journey_metric['runtimes'] if journey_metric.get("runtimes") else ''
		event['config']['target_services'] = journey_metric['services'] if journey_metric.get("services") else ''
		event['config']['event_id'] = journey_metric['event_id'] if journey_metric.get("event_id") else ''
		event['config']['event_organizer'] = journey_metric['event_organizer'] if journey_metric.get("event_organizer") else ''
	except:
		pass
	return event