import React, { useState, useEffect } from 'react';
import { ThemeContext } from '../contexts/ThemeContext';
import type { ColorScheme } from '../contexts/ThemeContext';

interface ThemeProviderProps {
  children: React.ReactNode;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  const [colorScheme, setColorScheme] = useState<ColorScheme>(() => {
    try {
      const saved = localStorage.getItem('mantine-color-scheme');
      if (saved === 'light' || saved === 'dark') {
        return saved;
      }
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    } catch {
      return 'light';
    }
  });

  const toggleColorScheme = () => {
    const newScheme: ColorScheme = colorScheme === 'dark' ? 'light' : 'dark';
    setColorScheme(newScheme);
    try {
      localStorage.setItem('mantine-color-scheme', newScheme);
    } catch {
      // Ignore write errors (e.g., storage full / disabled)
    }
  };

  useEffect(() => {
    // Listen for system theme changes
    try {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      const handleChange = (e: MediaQueryListEvent) => {
        try {
          const saved = localStorage.getItem('mantine-color-scheme');
          if (!saved) {
            setColorScheme(e.matches ? 'dark' : 'light');
          }
        } catch {
          // ignore
        }
      };
      mediaQuery.addEventListener('change', handleChange);
      return () => mediaQuery.removeEventListener('change', handleChange);
    } catch {
      return () => {};
    }
  }, []);

  return (
    <ThemeContext.Provider value={{ colorScheme, toggleColorScheme }}>
      {children}
    </ThemeContext.Provider>
  );
};
