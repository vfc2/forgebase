import { useState, useCallback } from 'react';
import type { Project } from '../types/api';

interface UseProjectsReturn {
  projects: Project[];
  currentProjectId: string | null;
  createProject: (name: string) => void;
  deleteProject: (id: string) => void;
  selectProject: (id: string) => void;
}

export const useProjects = (): UseProjectsReturn => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [currentProjectId, setCurrentProjectId] = useState<string | null>(null);

  const createProject = useCallback((name: string) => {
    const newProject: Project = {
      id: crypto.randomUUID(),
      name: name.trim(),
      createdAt: new Date(),
    };
    
    setProjects(prev => [newProject, ...prev]);
    setCurrentProjectId(newProject.id);
  }, []);

  const deleteProject = useCallback((id: string) => {
    setProjects(prev => prev.filter(project => project.id !== id));
    
    // If the deleted project was the current one, clear selection
    if (currentProjectId === id) {
      setCurrentProjectId(null);
    }
  }, [currentProjectId]);

  const selectProject = useCallback((id: string) => {
    setCurrentProjectId(id);
  }, []);

  return {
    projects,
    currentProjectId,
    createProject,
    deleteProject,
    selectProject,
  };
};
