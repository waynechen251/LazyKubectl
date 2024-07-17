# 包含命令生成器和命令執行器功能。命令生成器可以根據用戶操作生成 kubectl 命令，並將其傳遞給命令執行器來執行。這裡也可以處理命令的異常情況和錯誤處理。import subprocess
import subprocess
import json
from kubectlutils import KubectlUtils

class KubectlCommands:
  
  @staticmethod
  def run(caller, command):
    try:
      result = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8', timeout=15)
      return result
    except Exception as e:
      msg = f"kubectlcommands.{caller} error: {e}"
      print(msg)
      return msg
  
  @staticmethod
  def get_all_pods():
    try:
      result = KubectlCommands.run("get_all_pods", ["kubectl", "get", "pods", "-A", "-o", "json"])
      data = KubectlUtils.parse_get_all_pods(result.stdout)
      return data
    except Exception as e:
      print(f"kubectlcommands.get_all_pods error: {e}")
      return f"Error: {e}"
  
  @staticmethod
  def describe_pod(name, namespace):
    try:
      result = KubectlCommands.run("describe_pod", ["kubectl", "describe", "pod", name, "-n", namespace])
      return result.stdout
    except Exception as e:
      print(f"kubectlcommands.describe_pod error: {e}")
      return f"Error: {e}"
    
  @staticmethod
  def delete_pod(name, namespace):
    try:
      result = KubectlCommands.run("delete_pod", ["kubectl", "delete", "pod", name, "-n", namespace])
      return result.stdout
    except Exception as e:
      print(f"kubectlcommands.delete_pod error: {e}")
      return f"Error: {e}"
  
  @staticmethod
  def logs_pod(name, namespace):
    try:
      result = KubectlCommands.run("logs_pod", ["kubectl", "logs", name, "-n", namespace])
      return result.stdout
    except Exception as e:
      print(f"kubectlcommands.logs_pod error: {e}")
      return f"Error: {e}"