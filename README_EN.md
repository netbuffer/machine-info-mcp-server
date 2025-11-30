# machine-info-mcp-server

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Java](https://img.shields.io/badge/java-17%2B-orange)](https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.5.7-brightgreen)](https://spring.io/projects/spring-boot)
[![Spring AI](https://img.shields.io/badge/Spring%20AI-1.1.0-blueviolet)](https://spring.io/projects/spring-ai)
[![oshi](https://img.shields.io/badge/oshi-6.9.1-black)](https://github.com/oshi/oshi)

[中文文档](README.md)

A lightweight host information MCP tool that provides system information through the MCP (Model Context Protocol) interface, built with Spring Boot 3, Spring AI, and OSHI (Operating System and Hardware Information) library.

## Features

- Get detailed system information including:
  - CPU details (name, core count)
  - Memory usage (total, available)
  - Disk information for all mounted volumes (name, total space, used space, free space, usage percentage)
  - Operating system information
- Lightweight and fast
- Easy to integrate with Spring AI applications
- Provides MCP interface to access system information

## Prerequisites

- Java 17 or higher
- Maven 3.6.3 or higher

## Getting Started

### Build from Source

```bash
# Clone the repository
git clone https://github.com/netbuffer/machine-info-mcp-server.git
cd machine-info-mcp-server

# Build the project
mvn clean package

# Run the application
java -jar target/machine-info-mcp-server.jar
```

## API Endpoints

- `get_system_info` - Get host information

Example response:
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

## Configuration

Edit `src/main/resources/application.yaml` to customize the application settings:

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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Spring Boot](https://spring.io/projects/spring-boot)
- [Spring AI](https://spring.io/projects/spring-ai)
- [OSHI](https://github.com/oshi/oshi)

---
