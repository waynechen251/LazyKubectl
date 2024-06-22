# 其他工具函數的模組，例如結果解析器。這裡可以定義解析 kubectl 命令返回的結果，準備在 GUI 中顯示的格式。import json
import json

class KubectlUtils:
  @staticmethod
  def parse_namespaces(output):
    if output:
      try:
        # output = namespaces = ['argocd', 'default', 'digihua-smom-devops84blm', 'dotnet8-demorxrjk', 'kube-node-lease', 'kube-public', 'kube-system', 'kubekey-system', 'kubesphere-controls-system', 'kubesphere-devops-system', 'kubesphere-devops-worker', 'kubesphere-monitoring-federated', 'kubesphere-monitoring-system', 'kubesphere-system', 'lowcode']
        namespaces = json.loads(output)["items"]
        print(f"utils.parse_namespaces namespaces: {namespaces}")
        return [namespace["metadata"]["name"] for namespace in namespaces]
      except (json.JSONDecodeError, KeyError) as e:
        print(f"utils.parse_namespaces error: {e}")
        return f"Error parsing namespaces: {e}"
    else:
      return "No output to parse"
  
  @staticmethod
  def parse_pods(output):
    if output:
      try:
        pods = json.loads(output)["items"]
        result = [{"name": pod["metadata"]["name"], "status": pod["status"]["phase"], "age": pod["metadata"]["creationTimestamp"]} for pod in pods]
        print(f"utils.parse_pods result: {result}")
        return result
      except (json.JSONDecodeError, KeyError) as e:
        print(f"utils.parse_pods error: {e}")
        return f"Error parsing pods: {e}"
    else:
      return "No output to parse"