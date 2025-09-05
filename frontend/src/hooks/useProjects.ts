import { useState, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiService } from '../services/api';
import type { Project, ProjectCreateRequest } from '../types/api';

interface UseProjectsReturn {
  projects: Project[];
  currentProjectId: string | null;
  createProject: (name: string) => Promise<void>;
  deleteProject: (id: string) => Promise<void>;
  selectProject: (id: string) => void;
  isLoading: boolean;
  error: Error | null;
}

export const useProjects = (): UseProjectsReturn => {
  const [currentProjectId, setCurrentProjectId] = useState<string | null>(null);
  const queryClient = useQueryClient();

  // Query for fetching projects
  const {
    data: projects = [],
    isLoading,
    error
  } = useQuery({
    queryKey: ['projects'],
    queryFn: apiService.listProjects.bind(apiService),
    staleTime: 5 * 60 * 1000, // Consider data fresh for 5 minutes
  });

  // Mutation for creating projects
  const createProjectMutation = useMutation({
    mutationFn: async (name: string) => {
      const request: ProjectCreateRequest = { name: name.trim() };
      return apiService.createProject(request);
    },
    onSuccess: (newProject) => {
      // Update the projects list in the cache
      queryClient.setQueryData(['projects'], (oldProjects: Project[] = []) => 
        [newProject, ...oldProjects]
      );
      // Select the newly created project
      setCurrentProjectId(newProject.id);
    },
    onError: (error) => {
      console.error('Failed to create project:', error);
    }
  });

  // Mutation for deleting projects
  const deleteProjectMutation = useMutation({
    mutationFn: (id: string) => apiService.deleteProject(id),
    onSuccess: (_, deletedId) => {
      // Remove the project from the cache
      queryClient.setQueryData(['projects'], (oldProjects: Project[] = []) => 
        oldProjects.filter(project => project.id !== deletedId)
      );
      // If the deleted project was the current one, clear selection
      if (currentProjectId === deletedId) {
        setCurrentProjectId(null);
      }
    },
    onError: (error) => {
      console.error('Failed to delete project:', error);
    }
  });

  const createProject = useCallback(async (name: string) => {
    if (!name.trim()) return;
    await createProjectMutation.mutateAsync(name);
  }, [createProjectMutation]);

  const deleteProject = useCallback(async (id: string) => {
    await deleteProjectMutation.mutateAsync(id);
  }, [deleteProjectMutation]);

  const selectProject = useCallback((id: string) => {
    setCurrentProjectId(id);
  }, []);

  return {
    projects,
    currentProjectId,
    createProject,
    deleteProject,
    selectProject,
    isLoading,
    error
  };
};
