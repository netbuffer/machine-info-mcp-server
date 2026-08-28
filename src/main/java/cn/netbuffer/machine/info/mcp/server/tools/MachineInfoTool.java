package cn.netbuffer.machine.info.mcp.server.tools;

import org.springframework.ai.tool.annotation.Tool;
import org.springframework.stereotype.Component;
import oshi.SystemInfo;
import oshi.hardware.CentralProcessor;
import oshi.hardware.GlobalMemory;
import oshi.hardware.HardwareAbstractionLayer;
import oshi.software.os.OSFileStore;
import oshi.software.os.OperatingSystem;
import java.util.HashMap;
import java.util.Map;

@Component
public class MachineInfoTool {

    @Tool(name = "get_system_info", description = "获取本机系统信息,获取电脑配置信息,获取CPU信息，获取内存信息，获取磁盘信息,获取主机信息")
    public Map<String, String> getSystemInfo() {
        Map<String, String> systemInfo = new HashMap<>();

        try {
            SystemInfo systemInfoObj = new SystemInfo();
            HardwareAbstractionLayer hardware = systemInfoObj.getHardware();
            OperatingSystem operatingSystem = systemInfoObj.getOperatingSystem();

            // CPU信息
            CentralProcessor processor = hardware.getProcessor();
            systemInfo.put("cpu_cores", String.valueOf(processor.getLogicalProcessorCount()));
            systemInfo.put("cpu_name", processor.getProcessorIdentifier().getName());

            // 内存信息
            GlobalMemory memory = hardware.getMemory();
            long totalMemory = memory.getTotal();
            long availableMemory = memory.getAvailable();
            systemInfo.put("memory_total", String.valueOf(totalMemory / (1024 * 1024)) + " MB");
            systemInfo.put("memory_available", String.valueOf(availableMemory / (1024 * 1024)) + " MB");

            // 系统信息
            systemInfo.put("os_name", operatingSystem.getFamily());
            systemInfo.put("os_version", operatingSystem.getVersionInfo().getVersion());

            // 磁盘信息(获取所有磁盘信息)
            int diskIndex = 1;
            for (OSFileStore fs : operatingSystem.getFileSystem().getFileStores()) {
                String prefix = "disk" + diskIndex + "_";
                long total = fs.getTotalSpace();
                long free = fs.getFreeSpace();
                long used = total - free;
                double usedPercentage = total > 0 ? (used * 100.0 / total) : 0;
                
                systemInfo.put(prefix + "name", fs.getName());
                systemInfo.put(prefix + "total_gb", String.format("%.2f GB", total / (1024.0 * 1024 * 1024)));
                systemInfo.put(prefix + "free_gb", String.format("%.2f GB", free / (1024.0 * 1024 * 1024)));
                systemInfo.put(prefix + "used_gb", String.format("%.2f GB", used / (1024.0 * 1024 * 1024)));
                systemInfo.put(prefix + "used_percent", String.format("%.1f%%", usedPercentage));
                systemInfo.put(prefix + "type", fs.getType());
                systemInfo.put(prefix + "mount", fs.getMount());
                
                diskIndex++;
            }
            systemInfo.put("disk_count", String.valueOf(diskIndex - 1));

        } catch (Exception e) {
            systemInfo.put("error", "获取系统信息失败: " + e.getMessage());
        }

        return systemInfo;
    }

}