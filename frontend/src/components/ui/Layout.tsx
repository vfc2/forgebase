import React, { useState } from 'react';
import { AppShell } from '@mantine/core';
import { Header } from '../layout/Header';
import { Sidebar } from '../layout/Sidebar';
import { ChatInterface } from '../chat/ChatInterface';
import { useProjects } from '../../hooks/useProjects';

export const Layout: React.FC = () => {
    const [sidebarOpened] = useState(false);
    const { 
        projects, 
        currentProjectId, 
        createProject, 
        deleteProject, 
        selectProject
    } = useProjects();

    const handleNewProject = (name: string) => {
        createProject(name);
    };

    const handleProjectSelect = (projectId: string) => {
        selectProject(projectId);
    };

    const handleProjectDelete = (projectId: string) => {
        deleteProject(projectId);
    };

    const handleSettingsClick = () => {
        // TODO: Implement settings functionality
        console.log('Settings clicked');
    };

    const handleProfileClick = () => {
        // TODO: Implement profile functionality
        console.log('Profile clicked');
    };

    return (
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
            />

            <AppShell.Main
                style={{
                    display: 'flex',
                    flexDirection: 'column',
                    height: 'calc(100vh - 70px)'
                }}
            >
                <ChatInterface hasActiveProject={currentProjectId !== null} />
            </AppShell.Main>
        </AppShell>
    );
};
