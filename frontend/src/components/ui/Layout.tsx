import React, { useState } from 'react';
import { AppShell, Notification } from '@mantine/core';
import { IconX } from '@tabler/icons-react';
import { Header } from '../layout/Header';
import { Sidebar } from '../layout/Sidebar';
import { ChatInterface } from '../chat/ChatInterface';
import { ProjectStages } from '../project/ProjectStages';
import { useProjects } from '../../hooks/useProjects';

export const Layout: React.FC = () => {
    const [sidebarOpened] = useState(false);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);
    const { 
        projects, 
        currentProjectId, 
        createProject, 
        deleteProject, 
        selectProject,
        isLoading,
        error
    } = useProjects();

    const handleNewProject = async (name: string) => {
        try {
            await createProject(name);
        } catch (err) {
            const message = err instanceof Error ? err.message : 'Failed to create project';
            setErrorMessage(message);
        }
    };

    const handleProjectSelect = (projectId: string) => {
        selectProject(projectId);
    };

    const handleProjectDelete = async (projectId: string) => {
        try {
            await deleteProject(projectId);
        } catch (err) {
            const message = err instanceof Error ? err.message : 'Failed to delete project';
            setErrorMessage(message);
        }
    };

    const handleSettingsClick = () => {
        // TODO: Implement settings functionality
        console.log('Settings clicked');
    };

    const handleProfileClick = () => {
        // TODO: Implement profile functionality
        console.log('Profile clicked');
    };

    // Show error from useProjects hook or local operations
    const displayError = error?.message || errorMessage;

    return (
        <>
            {displayError && (
                <Notification
                    icon={<IconX size="1.1rem" />}
                    color="red"
                    title="Error"
                    onClose={() => setErrorMessage(null)}
                    style={{
                        position: 'fixed',
                        top: 20,
                        right: 20,
                        zIndex: 1000,
                    }}
                >
                    {displayError}
                </Notification>
            )}
            
            <AppShell
                header={{ height: 70 }}
                navbar={{
                    width: 280,
                    breakpoint: 'sm',
                    collapsed: { mobile: !sidebarOpened }
                }}
                padding="0"
                styles={{
                    main: {
                        backgroundColor: 'light-dark(#fcfcfc, var(--mantine-color-dark-7))'
                    },
                    header: {
                        backgroundColor: 'light-dark(#f8f9fa, var(--mantine-color-dark-7))',
                        borderColor: 'light-dark(#e8eaed, var(--mantine-color-dark-5))'
                    },
                    navbar: {
                        backgroundColor: 'light-dark(#f8f9fa, var(--mantine-color-dark-8))',
                        borderColor: 'light-dark(#e8eaed, var(--mantine-color-dark-5))'
                    }
                }}
            >
                <Header 
                    onSettingsClick={handleSettingsClick}
                    onProfileClick={handleProfileClick}
                />
                
                <Sidebar
                    onNewProject={handleNewProject}
                    projects={projects}
                    onProjectSelect={handleProjectSelect}
                    onProjectDelete={handleProjectDelete}
                    currentProjectId={currentProjectId}
                    isLoading={isLoading}
                />

                <AppShell.Main
                    style={{
                        display: 'flex',
                        flexDirection: 'column',
                        height: 'calc(100vh - 70px)'
                    }}
                >
                    {currentProjectId ? (
                        <ProjectStages projectId={currentProjectId} />
                    ) : (
                        <ChatInterface projectId={null} />
                    )}
                </AppShell.Main>
            </AppShell>
        </>
    );
};
