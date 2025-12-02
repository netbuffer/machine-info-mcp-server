# machine-info-mcp-server

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Java](https://img.shields.io/badge/java-17%2B-orange)](https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.5.7-brightgreen)](https://spring.io/projects/spring-boot)
[![Spring AI](https://img.shields.io/badge/Spring%20AI-1.1.0-blueviolet)](https://spring.io/projects/spring-ai)
[![oshi](https://img.shields.io/badge/oshi-6.9.1-black)](https://github.com/oshi/oshi)

[English Documentation](README_EN.md)

一个轻量级的主机信息获取MCP工具，通过MCP（模型上下文协议）接口提供系统信息，基于Spring Boot3+Spring AI+OSHI（操作系统和硬件信息）库构建。

https://github.com/netbuffer/machine-info-mcp-server  
https://gitee.com/netbuffer/machine-info-mcp-server

## 功能特性

- 获取详细的系统信息，包括：
  - CPU详情（名称、核心数）
  - 内存使用情况（总量、可用量）
  - 所有挂载卷的磁盘信息（名称、总空间、已用空间、可用空间、使用率）
  - 操作系统信息
- 轻量级且快速
- 易于与Spring AI应用集成
- 提供MCP接口获取系统信息

## MCP客户端集成方法

### 配置说明
将如下JSON配置添加到MCP客户端的配置文件中（通常是`~/.mcp/config.json`或项目根目录下的`mcp.config.json`）：

```json
{
  "mcpServers": {
    "machine-info-mcp-server": {
      "command": "java",
      "args": [
        "-jar",
        "machine-info-mcp-server.jar"
      ],
      "env": {
        "JAVA_HOME": "/path/to/your/java17"  // 可选，如果系统未设置JAVA_HOME
      },
      "description": "获取系统信息的MCP服务"
    }
  }
}
```

### 配置项说明
- `command`: 启动命令（通常是`java`）
- `args`: 启动参数，`-jar` 后跟jar包路径
- `env`: 环境变量配置（可选）
- `description`: 服务描述（可选）

### 验证配置
保存配置文件后，应该能看到`get_system_info`工具在可用工具列表中。

## 环境要求

- Java 17 或更高版本
- Maven 3.6.3 或更高版本

## 快速开始

### 从源码构建

```bash
# 克隆仓库
git clone https://github.com/netbuffer/machine-info-mcp-server.git
cd machine-info-mcp-server

# 构建项目
mvn clean package

# 运行应用
java -jar target/machine-info-mcp-server.jar
```

## API接口

- `get_system_info` - 获取主机信息

响应示例：
```json
{
  "cpu_cores": "8",
  "cpu_name": "Intel(R) Core(TM) i7-10700K CPU @ 3.80GHz",
  "memory_total": "16384 MB",
  "memory_available": "8192 MB",
  "os_name": "Windows 10",
  "os_version": "10.0",
  "disk_count": "2",
  "disk1_name": "C:",
  "disk1_total_gb": "465.76 GB",
  "disk1_free_gb": "200.45 GB",
  "disk1_used_gb": "265.31 GB",
  "disk1_used_percent": "57.0%",
  "disk1_type": "NTFS",
  "disk1_mount": "C:\\"
}
```

## 配置

编辑 `src/main/resources/application.yaml` 自定义应用设置：

```yaml
spring:
  application:
    name: machine-info-mcp-server
  ai:
    mcp:
      server:
        enabled: true
        name: ${spring.application.name}
        version: 1.0.0
        type: async
        stdio: true
```

## 贡献

欢迎贡献代码！请随时提交Pull Request。

## 许可证

本项目采用MIT许可证 - 详情请参阅[LICENSE](LICENSE)文件。

## 致谢

- [Spring Boot](https://spring.io/projects/spring-boot)
- [Spring AI](https://spring.io/projects/spring-ai)
- [OSHI](https://github.com/oshi/oshi)

---
