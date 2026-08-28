#!/usr/bin/env python3
import json
import os
import platform
import shutil
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone, timedelta

def run_cmd(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
        return output.decode('utf-8', errors='ignore').strip()
    except Exception:
        return "N/A"

def get_public_ip():
    try:
        req = urllib.request.Request("https://api.ipify.org", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.read().decode('utf-8').strip()
    except Exception:
        return "N/A"

def main():
    webhook = os.environ.get('DINGTALK_WEBHOOK', '').strip()
    if not webhook:
        print("⚠️ DINGTALK_WEBHOOK is empty. Skipping notification.")
        sys.exit(0)

    # 1. 收集 GitHub 事件上下文与时间戳
    beijing_tz = timezone(timedelta(hours=8))
    now_str = datetime.now(beijing_tz).strftime("%Y-%m-%d %H:%M:%S (CST/北京时间)")

    job_status = os.environ.get('JOB_STATUS', 'success')
    emoji = "🚀" if job_status == 'success' else "💥"
    status_text = "构建与测试成功" if job_status == 'success' else "构建或测试失败"

    repo = os.environ.get('GITHUB_REPOSITORY', 'N/A')
    event_name = os.environ.get('GITHUB_EVENT_NAME', 'N/A')
    actor = os.environ.get('GITHUB_ACTOR', 'N/A')
    ref_name = os.environ.get('GITHUB_REF_NAME', 'N/A')
    sha_full = os.environ.get('GITHUB_SHA', '')
    sha_short = sha_full[:8] if sha_full else 'N/A'
    run_id = os.environ.get('GITHUB_RUN_ID', 'N/A')
    run_number = os.environ.get('GITHUB_RUN_NUMBER', 'N/A')
    run_attempt = os.environ.get('GITHUB_RUN_ATTEMPT', '1')

    # 2. 收集系统与硬件信息
    os_pretty = run_cmd("cat /etc/os-release | grep PRETTY_NAME | cut -d'\"' -f2")
    if os_pretty == "N/A":
        os_pretty = platform.platform()
    
    kernel_ver = platform.release() or run_cmd("uname -sr")
    hostname_val = platform.node() or run_cmd("hostname")
    uptime_val = run_cmd("uptime -p")

    cpu_model = run_cmd("lscpu | grep 'Model name' | sed 's/Model name:\s*//'")
    if cpu_model == "N/A":
        cpu_model = platform.processor() or "CPU"
    
    cpu_cores = os.cpu_count() or run_cmd("nproc")
    cpu_mhz = run_cmd("lscpu | grep 'CPU max MHz' | awk '{print $4}'")
    mem_summary = run_cmd("free -h | awk '/Mem:/ {print \"总量: \"$2\" | 已用: \"$3\" | 空闲: \"$4\" | 可用: \"$7}'")
    swap_summary = run_cmd("free -h | awk '/Swap:/ {print \"总量: \"$2\" | 已用: \"$3\" | 空闲: \"$4}'")
    disk_root = run_cmd("df -h / | awk 'NR==2 {print \"总量: \"$2\" | 已用: \"$3\" (\"$5\") | 剩余: \"$4}'")

    # 3. 网络信息
    public_ip = get_public_ip()
    local_ip = run_cmd("hostname -I | awk '{print $1}'")

    # 4. 工具与运行环境版本
    java_ver = run_cmd("java -version 2>&1 | head -n 1")
    mvn_ver = run_cmd("mvn -version 2>&1 | head -n 1")
    node_ver = run_cmd("node -v")
    python_ver = platform.python_version()
    docker_ver = run_cmd("docker --version")
    git_ver = run_cmd("git --version")

    # 终端本地日志打印
    print("=======================================================")
    print("         🔍 GITHUB ACTIONS RUNNER COMPLETE INFO        ")
    print("=======================================================")
    print(f"📌 Repo        : {repo}")
    print(f"📌 Event / Actor: {event_name} / {actor}")
    print(f"📌 Ref / SHA   : {ref_name} ({sha_short})")
    print(f"💻 OS / Kernel : {os_pretty} / {kernel_ver}")
    print(f"⚡ CPU / Cores : {cpu_model} ({cpu_cores} Cores)")
    print(f"🧠 Memory      : {mem_summary}")
    print(f"💽 Disk        : {disk_root}")
    print(f"🌐 Public IP   : {public_ip}")
    print(f"☕ Java        : {java_ver}")
    print(f"📦 Maven       : {mvn_ver}")
    print("=======================================================")

    # 5. 构建钉钉 Markdown 消息
    lines = [
        f"### {emoji} GitHub Actions 每日综合巡检报告",
        f"> **项目仓库**: [{repo}](https://github.com/{repo})",
        f"> **运行状态**: **{status_text}** (第 #{run_number} 次运行 / 尝试 #{run_attempt})",
        f"> **执行时间**: ⏰ `{now_str}`",
        "---",
        "#### 📌 [1] 触发与运行上下文",
        f"- 👤 **触发用户**: `{actor}`",
        f"- ⚡ **触发事件**: `{event_name}`",
        f"- 🌿 **分支/Tag**: `{ref_name}` (Commit: [`{sha_short}`](https://github.com/{repo}/commit/{sha_full}))",
        f"- 🔗 **Run 详情**: [点击查看运行日志](https://github.com/{repo}/actions/runs/{run_id})",
        "---",
        "#### 🖥️ [2] Runner 服务器硬件与系统配置",
        f"- 🐧 **操作系统**: `{os_pretty}`",
        f"- ⚙️ **内核版本**: `{kernel_ver}`",
        f"- 💻 **主机名称**: `{hostname_val}`",
        f"- ⚡ **CPU 处理器**: `{cpu_model}` (`{cpu_cores}` 核 / `{cpu_mhz}` MHz)",
        f"- 🧠 **内存空间**: `{mem_summary}`",
        f"- 💾 **交换分区**: `{swap_summary}`",
        f"- 💽 **根磁盘容量**: `{disk_root}`",
        f"- ⏱️ **系统运行时间**: `{uptime_val}`",
        "---",
        "#### 🌐 [3] 网络与出口地址",
        f"- 🌍 **Runner 公网 IP**: `{public_ip}`",
        f"- 🏠 **Runner 内网 IP**: `{local_ip}`",
        "---",
        "#### 🛠️ [4] 预装预置开发工具链",
        f"- ☕ **Java 环境**: `{java_ver}`",
        f"- 📦 **Maven 版本**: `{mvn_ver}`",
        f"- 🟢 **Node.js**: `{node_ver}`",
        f"- 🐍 **Python3**: `{python_ver}`",
        f"- 🐳 **Docker**: `{docker_ver}`",
        f"- 🔀 **Git 工具**: `{git_ver}`",
        "---",
        "*来自 Machine Info MCP Server CI/CD 自动化系统*"
    ]

    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": f"{emoji} GitHub Actions 综合巡检报告",
            "text": "\n".join(lines)
        }
    }

    try:
        req = urllib.request.Request(
            webhook,
            data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            res_content = resp.read().decode('utf-8')
            print(f"DingTalk Response: {res_content}")
    except Exception as e:
        print(f"❌ Failed to send DingTalk notice: {e}")

if __name__ == "__main__":
    main()
