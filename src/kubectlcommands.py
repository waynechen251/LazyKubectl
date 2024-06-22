# 包含命令生成器和命令執行器功能。命令生成器可以根據用戶操作生成 kubectl 命令，並將其傳遞給命令執行器來執行。這裡也可以處理命令的異常情況和錯誤處理。import subprocess
import subprocess
import json

class KubectlCommands:
  @staticmethod
  def get_namespaces():
    try:
      result = subprocess.run(["kubectl", "get", "namespaces", "-o", "json"], capture_output=True, text=True, check=True, encoding='utf-8')
      result_json = json.loads(result.stdout)
      print(f"kubectlcommands.get_namespaces result_json: {result_json}")
      return result_json
    except subprocess.CalledProcessError as e:
      return f"Error: {e}"
  
  def get_pods():
    try:
      result = subprocess.run(["kubectl", "get", "pods", "-o", "json"], capture_output=True, text=True, check=True, encoding='utf-8')
      result_json = json.loads(result.stdout)
      print(f"kubectlcommands.get_pods result_json: {result_json}")
      return result_json
    except subprocess.CalledProcessError as e:
      print(f"kubectlcommands.get_pods error: {e}")
      return f"Error: {e}"