import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { userEvent } from '@testing-library/user-event';
import { MantineProvider, AppShell } from '@mantine/core';
import { Sidebar } from './Sidebar';
import type { Project } from '../../types/api';

// Wrapper component for Mantine provider and AppShell context
const TestWrapper = ({ children }: { children: React.ReactNode }) => (
    <MantineProvider>
        <AppShell>
            {children}
        </AppShell>
    </MantineProvider>
);

const mockProjects: Project[] = [
    {
        id: '1',
        name: 'E-commerce Platform PRD',
        createdAt: new Date(2025, 8, 1)
    },
    {
        id: '2',
        name: 'Mobile App Requirements',
        createdAt: new Date(2025, 8, 2)
    }
];

describe('Sidebar', () => {
    it('renders the New Project button', () => {
        const onNewProject = vi.fn();
        
        render(
            <TestWrapper>
                <Sidebar onNewProject={onNewProject} />
            </TestWrapper>
        );
        
        expect(screen.getByText('New Project')).toBeInTheDocument();
    });

    it('opens new project modal when New Project button is clicked', async () => {
        const user = userEvent.setup();
        const onNewProject = vi.fn();
        
        render(
            <TestWrapper>
                <Sidebar onNewProject={onNewProject} />
            </TestWrapper>
        );
        
        await user.click(screen.getByText('New Project'));
        
        // Wait for modal to appear using more flexible text matching
        expect(await screen.findByText(/Create New Project/)).toBeInTheDocument();
        expect(await screen.findByPlaceholderText('Enter project name...')).toBeInTheDocument();
    });

    it('displays "No projects yet" when projects list is empty', () => {
        render(
            <TestWrapper>
                <Sidebar onNewProject={vi.fn()} projects={[]} />
            </TestWrapper>
        );
        
        expect(screen.getByText('No projects yet')).toBeInTheDocument();
    });

    it('displays projects when provided', () => {
        render(
            <TestWrapper>
                <Sidebar 
                    onNewProject={vi.fn()} 
                    projects={mockProjects}
                />
            </TestWrapper>
        );
        
        expect(screen.getByText('E-commerce Platform PRD')).toBeInTheDocument();
        expect(screen.getByText('Mobile App Requirements')).toBeInTheDocument();
    });

    it('calls onProjectSelect when a project is clicked', async () => {
        const user = userEvent.setup();
        const onProjectSelect = vi.fn();
        
        render(
            <TestWrapper>
                <Sidebar 
                    onNewProject={vi.fn()}
                    projects={mockProjects}
                    onProjectSelect={onProjectSelect}
                />
            </TestWrapper>
        );
        
        await user.click(screen.getByText('E-commerce Platform PRD'));
        expect(onProjectSelect).toHaveBeenCalledWith('1');
    });

    it('highlights the current project', () => {
        render(
            <TestWrapper>
                <Sidebar 
                    onNewProject={vi.fn()}
                    projects={mockProjects}
                    currentProjectId="1"
                />
            </TestWrapper>
        );
        
        const currentProjectButton = screen.getByText('E-commerce Platform PRD').closest('button');
        expect(currentProjectButton).toHaveAttribute('data-variant', 'light');
    });

    it('does not show clear projects button', () => {
        render(
            <TestWrapper>
                <Sidebar 
                    onNewProject={vi.fn()}
                    projects={mockProjects}
                />
            </TestWrapper>
        );
        
        expect(screen.queryByLabelText('Clear Projects')).not.toBeInTheDocument();
    });

    it('creates a project when form is submitted with valid name', async () => {
        const user = userEvent.setup();
        const onNewProject = vi.fn();
        
        render(
            <TestWrapper>
                <Sidebar onNewProject={onNewProject} />
            </TestWrapper>
        );
        
        // Open modal
        await user.click(screen.getByText('New Project'));
        
        // Fill in project name using placeholder text
        const nameInput = await screen.findByPlaceholderText('Enter project name...');
        await user.type(nameInput, 'Test Project');
        
        // Submit form
        await user.click(await screen.findByText('Create Project'));
        
        expect(onNewProject).toHaveBeenCalledWith('Test Project');
    });

    it('creates a project when Enter key is pressed in name input', async () => {
        const user = userEvent.setup();
        const onNewProject = vi.fn();
        
        render(
            <TestWrapper>
                <Sidebar onNewProject={onNewProject} />
            </TestWrapper>
        );
        
        // Open modal
        await user.click(screen.getByText('New Project'));
        
        // Fill in project name and press Enter
        const nameInput = await screen.findByPlaceholderText('Enter project name...');
        await user.type(nameInput, 'Test Project{enter}');
        
        expect(onNewProject).toHaveBeenCalledWith('Test Project');
    });

    it('does not create project when form is submitted with empty name', async () => {
        const user = userEvent.setup();
        const onNewProject = vi.fn();
        
        render(
            <TestWrapper>
                <Sidebar onNewProject={onNewProject} />
            </TestWrapper>
        );
        
        // Open modal
        await user.click(screen.getByText('New Project'));
        
        // Try to create project with empty name
        const createButton = await screen.findByText('Create Project');
        await user.click(createButton);
        
        // Should not call onNewProject
        expect(onNewProject).not.toHaveBeenCalled();
    });

    it('shows delete confirmation when delete is clicked', async () => {
        const user = userEvent.setup();
        
        render(
            <TestWrapper>
                <Sidebar 
                    onNewProject={vi.fn()}
                    projects={mockProjects}
                    onProjectDelete={vi.fn()}
                />
            </TestWrapper>
        );
        
        // Click on project options menu (dots button)
        const optionsButton = screen.getByLabelText('Project options for E-commerce Platform PRD');
        await user.click(optionsButton);
        
        // Click delete option - find by role since menu item text might not be visible
        const deleteButton = await screen.findByRole('menuitem', { name: /Delete Project/ });
        await user.click(deleteButton);
        
        // Check for delete confirmation modal
        expect(await screen.findByText(/Are you sure you want to delete this project/)).toBeInTheDocument();
        expect(await screen.findByRole('button', { name: 'Delete' })).toBeInTheDocument();
    });

    it('calls onProjectDelete when delete is confirmed', async () => {
        const user = userEvent.setup();
        const onProjectDelete = vi.fn();
        
        render(
            <TestWrapper>
                <Sidebar 
                    onNewProject={vi.fn()}
                    projects={mockProjects}
                    onProjectDelete={onProjectDelete}
                />
            </TestWrapper>
        );
        
        // Click on project options menu (dots button)
        const optionsButton = screen.getByLabelText('Project options for E-commerce Platform PRD');
        await user.click(optionsButton);
        
        // Click delete option
        const deleteButton = await screen.findByRole('menuitem', { name: /Delete Project/ });
        await user.click(deleteButton);
        
        // Confirm deletion
        const confirmButton = await screen.findByRole('button', { name: 'Delete' });
        await user.click(confirmButton);
        
        expect(onProjectDelete).toHaveBeenCalledWith('1');
    });

    it('renders quick action buttons', () => {
        render(
            <TestWrapper>
                <Sidebar onNewProject={vi.fn()} />
            </TestWrapper>
        );
        
        expect(screen.getByText('Tips & Examples')).toBeInTheDocument();
        expect(screen.getByText('Export Project')).toBeInTheDocument();
        expect(screen.getByText('Preferences')).toBeInTheDocument();
    });
});
