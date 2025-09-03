import { describe, it, expect, beforeEach, vi } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useProjects } from './useProjects';

// Mock crypto.randomUUID
const mockUUID = vi.fn();
Object.defineProperty(globalThis, 'crypto', {
  value: {
    randomUUID: mockUUID,
  },
  writable: true,
});

describe('useProjects', () => {
  beforeEach(() => {
    mockUUID.mockClear();
    mockUUID.mockReturnValue('mock-uuid-123');
  });

  it('initializes with empty projects array and no current project', () => {
    const { result } = renderHook(() => useProjects());
    
    expect(result.current.projects).toEqual([]);
    expect(result.current.currentProjectId).toBeNull();
  });

  it('creates a new project and sets it as current', () => {
    const { result } = renderHook(() => useProjects());
    
    act(() => {
      result.current.createProject('Test Project');
    });

    expect(result.current.projects).toHaveLength(1);
    expect(result.current.projects[0]).toEqual({
      id: 'mock-uuid-123',
      name: 'Test Project',
      createdAt: expect.any(Date),
    });
    expect(result.current.currentProjectId).toBe('mock-uuid-123');
  });

  it('trims whitespace from project names', () => {
    const { result } = renderHook(() => useProjects());
    
    act(() => {
      result.current.createProject('  Test Project  ');
    });

    expect(result.current.projects[0].name).toBe('Test Project');
  });

  it('adds new projects to the beginning of the list', () => {
    const { result } = renderHook(() => useProjects());
    
    mockUUID.mockReturnValueOnce('uuid-1');
    act(() => {
      result.current.createProject('Project 1');
    });

    mockUUID.mockReturnValueOnce('uuid-2');
    act(() => {
      result.current.createProject('Project 2');
    });

    expect(result.current.projects).toHaveLength(2);
    expect(result.current.projects[0].id).toBe('uuid-2');
    expect(result.current.projects[1].id).toBe('uuid-1');
  });

  it('deletes a project', () => {
    const { result } = renderHook(() => useProjects());
    
    mockUUID.mockReturnValueOnce('uuid-1');
    act(() => {
      result.current.createProject('Project 1');
    });

    mockUUID.mockReturnValueOnce('uuid-2');
    act(() => {
      result.current.createProject('Project 2');
    });

    act(() => {
      result.current.deleteProject('uuid-1');
    });

    expect(result.current.projects).toHaveLength(1);
    expect(result.current.projects[0].id).toBe('uuid-2');
  });

  it('clears current project when deleting the current project', () => {
    const { result } = renderHook(() => useProjects());
    
    mockUUID.mockReturnValueOnce('uuid-1');
    act(() => {
      result.current.createProject('Project 1');
    });

    expect(result.current.currentProjectId).toBe('uuid-1');

    act(() => {
      result.current.deleteProject('uuid-1');
    });

    expect(result.current.currentProjectId).toBeNull();
  });

  it('keeps current project when deleting a different project', () => {
    const { result } = renderHook(() => useProjects());
    
    mockUUID.mockReturnValueOnce('uuid-1');
    act(() => {
      result.current.createProject('Project 1');
    });

    mockUUID.mockReturnValueOnce('uuid-2');
    act(() => {
      result.current.createProject('Project 2');
    });

    act(() => {
      result.current.selectProject('uuid-1');
    });

    act(() => {
      result.current.deleteProject('uuid-2');
    });

    expect(result.current.currentProjectId).toBe('uuid-1');
  });

  it('selects a project', () => {
    const { result } = renderHook(() => useProjects());
    
    mockUUID.mockReturnValueOnce('uuid-1');
    act(() => {
      result.current.createProject('Project 1');
    });

    act(() => {
      result.current.selectProject('uuid-1');
    });

    expect(result.current.currentProjectId).toBe('uuid-1');
  });
});
