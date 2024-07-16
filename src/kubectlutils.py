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
            except Exception as e:
                msg = f"utils.parse_get_all_pods error: {e}"
                print(msg)
                return msg
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
        days = age.days
        hours, remainder = divmod(age.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{days}d {hours:02}h {minutes:02}m {seconds:02}s"


    @staticmethod
    def get_readiness_gates(conditions):
        gates = [condition["type"] for condition in conditions if condition["status"] != "True"]
        return ", ".join(gates) if gates else "N/A"
