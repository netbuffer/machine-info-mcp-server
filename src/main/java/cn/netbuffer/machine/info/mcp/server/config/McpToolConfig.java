package cn.netbuffer.machine.info.mcp.server.config;

import cn.netbuffer.machine.info.mcp.server.tools.MachineInfoTool;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class McpToolConfig {

    @Bean
    public ToolCallbackProvider buildToolCallbackProvider(MachineInfoTool dateTimeTool) {
        return MethodToolCallbackProvider.builder().toolObjects(dateTimeTool).build();
    }

}
