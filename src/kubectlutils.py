import json
from datetime import datetime, timezone
from dateutil import parser

class KubectlUtils:

    @staticmethod
    def parse_get_all_pods(output):
        if output:
            try:
                pods = json.loads(output)["items"]
                result = []
                for pod in pods:
                    pod_info = {
                        "NAMESPACE": pod["metadata"]["namespace"],
                        "NAME": pod["metadata"]["name"],
                        "READY": KubectlUtils.get_ready_status(pod["status"]["containerStatuses"]),
                        "STATUS": pod["status"]["phase"],
                        "RESTARTS": KubectlUtils.get_restarts(pod["status"]["containerStatuses"]),
                        "AGE": KubectlUtils.calculate_age(pod["metadata"]["creationTimestamp"]),
                        "IP": pod["status"].get("podIP", "N/A"),
                        "NODE": pod["spec"].get("nodeName", "N/A"),
                        "NOMINATED NODE": pod["status"].get("nominatedNodeName", "N/A"),
                        "READINESS GATES": KubectlUtils.get_readiness_gates(pod["status"].get("conditions", []))
                    }
                    result.append(pod_info)
                return result
            except (json.JSONDecodeError, KeyError) as e:
                print(f"utils.parse_get_all_pods error: {e}")
                return f"Error parsing get pods wide: {e}"
        else:
            return "No output to parse"

    @staticmethod
    def get_ready_status(container_statuses):
        ready = sum(1 for status in container_statuses if status["ready"])
        total = len(container_statuses)
        return f"{ready}/{total}"

    @staticmethod
    def get_restarts(container_statuses):
        return sum(status["restartCount"] for status in container_statuses)

    @staticmethod
    def calculate_age(creation_timestamp):
        creation_time = parser.parse(creation_timestamp)
        now = datetime.now(timezone.utc)
        age = now - creation_time
        return str(age).split('.')[0]  # Format the age to remove microseconds

    @staticmethod
    def get_readiness_gates(conditions):
        gates = [condition["type"] for condition in conditions if condition["status"] != "True"]
        return ", ".join(gates) if gates else "N/A"
