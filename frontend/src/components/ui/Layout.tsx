import React from 'react';

interface LayoutProps {
    children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
    return (
        <div className="h-screen bg-gray-50 flex flex-col">
            {/* Header */}
            <header className="bg-white border-b border-gray-200 px-6 py-4">
                <div className="flex items-center justify-between">
                    <h1 className="text-xl font-semibold text-gray-900">
                        Forgebase Chat
                    </h1>
                    <div className="text-sm text-gray-500">
                        Conversational PRD Generation
                    </div>
                </div>
            </header>

            {/* Main content */}
            <main className="flex-1 overflow-hidden">
                {children}
            </main>
        </div>
    );
};
