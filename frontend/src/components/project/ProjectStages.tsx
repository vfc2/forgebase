import React, { useState } from 'react';
import { Tabs, Box } from '@mantine/core';
import { IconMessageCircle, IconFileText, IconList } from '@tabler/icons-react';
import { ChatInterface } from '../chat/ChatInterface';
import { PrdPreview } from './PrdPreview';
import { BacklogView } from './BacklogView';

interface ProjectStagesProps {
    projectId: string;
}

export const ProjectStages: React.FC<ProjectStagesProps> = ({ projectId }) => {
    const [activeTab, setActiveTab] = useState<string>('chat');

    return (
        <Box style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <Tabs 
                value={activeTab} 
                onChange={(value) => setActiveTab(value || 'chat')}
                style={{ height: '100%', display: 'flex', flexDirection: 'column' }}
            >
                <Tabs.List style={{ flexShrink: 0 }}>
                    <Tabs.Tab 
                        value="chat" 
                        leftSection={<IconMessageCircle size={16} />}
                    >
                        Chat
                    </Tabs.Tab>
                    <Tabs.Tab 
                        value="prd" 
                        leftSection={<IconFileText size={16} />}
                    >
                        PRD
                    </Tabs.Tab>
                    <Tabs.Tab 
                        value="backlog" 
                        leftSection={<IconList size={16} />}
                    >
                        Backlog
                    </Tabs.Tab>
                </Tabs.List>

                <Box style={{ flex: 1, overflow: 'hidden', height: '100%' }}>
                    {activeTab === 'chat' && (
                        <Box style={{ height: '100%' }}>
                            <ChatInterface projectId={projectId} />
                        </Box>
                    )}
                    
                    {activeTab === 'prd' && (
                        <Box style={{ height: '100%' }}>
                            <PrdPreview projectId={projectId} />
                        </Box>
                    )}
                    
                    {activeTab === 'backlog' && (
                        <Box style={{ height: '100%' }}>
                            <BacklogView projectId={projectId} />
                        </Box>
                    )}
                </Box>
            </Tabs>
        </Box>
    );
};
