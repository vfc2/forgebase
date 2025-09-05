import { describe, it, expect, beforeEach, vi } from 'vitest';
import { renderHook, act, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import React from 'react';
import { useProjects } from './useProjects';
import { apiService } from '../services/api';
import type { Project, ProjectCreateRequest } from '../types/api';

// Mock the API service
vi.mock('../services/api', () => ({
  apiService: {
    listProjects: vi.fn(),
    createProject: vi.fn(),
    deleteProject: vi.fn(),
  }
}));

const mockApiService = vi.mocked(apiService);

// Test wrapper with QueryClient
const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
      mutations: {
        retry: false,
      },
    },
  });

  return ({ children }: { children: React.ReactNode }) =>
    React.createElement(QueryClientProvider, { client: queryClient }, children);
};

describe('useProjects', () => {
  const mockProject: Project = {
    id: '123e4567-e89b-12d3-a456-426614174000',
    name: 'Test Project',
    createdAt: new Date('2023-01-01T00:00:00.000Z'),
    updatedAt: new Date('2023-01-02T00:00:00.000Z')
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('initializes with no current project', () => {
    mockApiService.listProjects.mockResolvedValue([]);
    
    const { result } = renderHook(() => useProjects(), {
      wrapper: createWrapper(),
    });
    
    expect(result.current.currentProjectId).toBeNull();
    expect(result.current.isLoading).toBe(true);
  });

  it('loads projects from API on mount', async () => {
    mockApiService.listProjects.mockResolvedValue([mockProject]);
    
    const { result } = renderHook(() => useProjects(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.projects).toEqual([mockProject]);
    expect(mockApiService.listProjects).toHaveBeenCalledOnce();
  });

  it('creates a new project and sets it as current', async () => {
    mockApiService.listProjects.mockResolvedValue([]);
    mockApiService.createProject.mockResolvedValue(mockProject);
    
    const { result } = renderHook(() => useProjects(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    await act(async () => {
      await result.current.createProject('Test Project');
    });

    const expectedRequest: ProjectCreateRequest = { name: 'Test Project' };
    expect(mockApiService.createProject).toHaveBeenCalledWith(expectedRequest);
    expect(result.current.currentProjectId).toBe(mockProject.id);
    expect(result.current.projects).toContain(mockProject);
  });

  it('trims whitespace from project names', async () => {
    mockApiService.listProjects.mockResolvedValue([]);
    mockApiService.createProject.mockResolvedValue(mockProject);
    
    const { result } = renderHook(() => useProjects(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    await act(async () => {
      await result.current.createProject('  Test Project  ');
    });

    const expectedRequest: ProjectCreateRequest = { name: 'Test Project' };
    expect(mockApiService.createProject).toHaveBeenCalledWith(expectedRequest);
  });

  it('does not create project with empty name', async () => {
    mockApiService.listProjects.mockResolvedValue([]);
    
    const { result } = renderHook(() => useProjects(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    await act(async () => {
      await result.current.createProject('   ');
    });

    expect(mockApiService.createProject).not.toHaveBeenCalled();
  });

  it('deletes a project and clears current selection if deleted project was current', async () => {
    mockApiService.listProjects.mockResolvedValue([mockProject]);
    mockApiService.deleteProject.mockResolvedValue();
    
    const { result } = renderHook(() => useProjects(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    // Select the project first
    act(() => {
      result.current.selectProject(mockProject.id);
    });

    expect(result.current.currentProjectId).toBe(mockProject.id);

    // Delete the project
    await act(async () => {
      await result.current.deleteProject(mockProject.id);
    });

    expect(mockApiService.deleteProject).toHaveBeenCalledWith(mockProject.id);
    expect(result.current.currentProjectId).toBeNull();
  });

  it('deletes a project without affecting current selection if different project was current', async () => {
    const anotherProject = { ...mockProject, id: 'another-id', name: 'Another Project' };
    mockApiService.listProjects.mockResolvedValue([mockProject, anotherProject]);
    mockApiService.deleteProject.mockResolvedValue();
    
    const { result } = renderHook(() => useProjects(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    // Select a different project
    act(() => {
      result.current.selectProject(anotherProject.id);
    });

    expect(result.current.currentProjectId).toBe(anotherProject.id);

    // Delete the first project
    await act(async () => {
      await result.current.deleteProject(mockProject.id);
    });

    expect(mockApiService.deleteProject).toHaveBeenCalledWith(mockProject.id);
    expect(result.current.currentProjectId).toBe(anotherProject.id);
  });

  it('handles API errors gracefully', async () => {
    mockApiService.listProjects.mockRejectedValue(new Error('API Error'));
    
    const { result } = renderHook(() => useProjects(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.error).toBeInstanceOf(Error);
    expect(result.current.error?.message).toBe('API Error');
  });
});
