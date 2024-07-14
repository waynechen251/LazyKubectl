# 包含命令生成器和命令執行器功能。命令生成器可以根據用戶操作生成 kubectl 命令，並將其傳遞給命令執行器來執行。這裡也可以處理命令的異常情況和錯誤處理。import subprocess
import subprocess
import json
from kubectlutils import KubectlUtils

class KubectlCommands:

  @staticmethod
  def get_all_pods():
    try:
      result = subprocess.run(["kubectl", "get", "pods", "-A", "-o", "json"], capture_output=True, text=True, check=True, encoding='utf-8', timeout=15)
      data = KubectlUtils.parse_get_all_pods(result)
      return data
    except subprocess.CalledProcessError as e:
      print(f"kubectlcommands.get_all_pods error: {e}")
      return f"Error: {e}"
    except subprocess.TimeoutExpired as e:
      print(f"kubectlcommands.get_all_pods timeout: {e}")
      return f"Error: {e}"
  
  @staticmethod
  def describe_pod(name, namespace):
    try:
      result = subprocess.run(["kubectl", "describe", "pod", name, "-n", namespace], capture_output=True, text=True, check=True, encoding='utf-8', timeout=15)
      return result.stdout
    except subprocess.CalledProcessError as e:
      print(f"kubectlcommands.describe_pod error: {e}")
      return f"Error: {e}"
    except subprocess.TimeoutExpired as e:
      print(f"kubectlcommands.describe_pod timeout: {e}")
      return f"Error: {e}"