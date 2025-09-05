import React, { useState } from 'react';
import { Tabs, Box } from '@mantine/core';
import { IconMessageCircle, IconFileText, IconClipboardList } from '@tabler/icons-react';
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
                styles={{
                    root: {
                        backgroundColor: 'light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-8))',
                    },
                    list: {
                        backgroundColor: 'light-dark(var(--mantine-color-gray-1), var(--mantine-color-dark-7))',
                        borderBottom: '2px solid light-dark(var(--mantine-color-gray-3), var(--mantine-color-dark-5))',
                        padding: '8px 16px',
                        gap: '4px',
                        borderRadius: '0',
                        margin: '0',
                        flexShrink: 0,
                    },
                    tab: {
                        fontWeight: 500,
                        fontSize: '14px',
                        padding: '12px 20px',
                        borderRadius: '8px',
                        border: 'none',
                        backgroundColor: 'transparent',
                        color: 'light-dark(var(--mantine-color-gray-6), var(--mantine-color-gray-4))',
                        transition: 'all 0.2s ease',
                        position: 'relative',
                        '&:hover': {
                            backgroundColor: 'light-dark(var(--mantine-color-gray-2), var(--mantine-color-dark-6))',
                            color: 'light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-2))',
                        },
                    },
                    tabSection: {
                        marginRight: '8px',
                    }
                }}
                activateTabWithKeyboard={false}
            >
                <Tabs.List>
                    <Tabs.Tab 
                        value="chat" 
                        leftSection={<IconMessageCircle size={18} stroke={1.5} />}
                        style={{
                            ...(activeTab === 'chat' && {
                                backgroundColor: 'light-dark(var(--mantine-color-blue-1), var(--mantine-color-blue-9))',
                                color: 'light-dark(var(--mantine-color-blue-6), var(--mantine-color-blue-3))',
                                boxShadow: 'light-dark(0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.3))',
                            })
                        }}
                    >
                        Chat
                    </Tabs.Tab>
                    <Tabs.Tab 
                        value="prd" 
                        leftSection={<IconFileText size={18} stroke={1.5} />}
                        style={{
                            ...(activeTab === 'prd' && {
                                backgroundColor: 'light-dark(var(--mantine-color-blue-1), var(--mantine-color-blue-9))',
                                color: 'light-dark(var(--mantine-color-blue-6), var(--mantine-color-blue-3))',
                                boxShadow: 'light-dark(0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.3))',
                            })
                        }}
                    >
                        PRD
                    </Tabs.Tab>
                    <Tabs.Tab 
                        value="backlog" 
                        leftSection={<IconClipboardList size={18} stroke={1.5} />}
                        style={{
                            ...(activeTab === 'backlog' && {
                                backgroundColor: 'light-dark(var(--mantine-color-blue-1), var(--mantine-color-blue-9))',
                                color: 'light-dark(var(--mantine-color-blue-6), var(--mantine-color-blue-3))',
                                boxShadow: 'light-dark(0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.3))',
                            })
                        }}
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
