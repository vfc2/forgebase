import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import rehypeHighlight from 'rehype-highlight';
import { Button } from '../ui/Button';

interface MarkdownPreviewProps {
    content?: string;
}

export const MarkdownPreview: React.FC<MarkdownPreviewProps> = ({ content }) => {
    const [copied, setCopied] = useState(false);

    const handleCopy = async () => {
        if (content) {
            try {
                await navigator.clipboard.writeText(content);
                setCopied(true);
                setTimeout(() => setCopied(false), 2000);
            } catch (err) {
                console.error('Failed to copy content:', err);
            }
        }
    };

    if (!content) {
        return (
            <div className="h-full flex flex-col">
                <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200 bg-white">
                    <h2 className="text-lg font-medium text-gray-900">
                        Markdown Preview
                    </h2>
                </div>
                <div className="flex-1 flex items-center justify-center text-gray-500">
                    <div className="text-center">
                        <div className="text-lg font-medium mb-2">
                            No content to preview
                        </div>
                        <div className="text-sm">
                            Markdown content will appear here when available
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="h-full flex flex-col">
            {/* Header with copy button */}
            <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200 bg-white">
                <h2 className="text-lg font-medium text-gray-900">
                    Markdown Preview
                </h2>
                <Button
                    variant="ghost"
                    size="sm"
                    onClick={handleCopy}
                    disabled={!content}
                >
                    {copied ? (
                        <>
                            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                            </svg>
                            Copied!
                        </>
                    ) : (
                        <>
                            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                            </svg>
                            Copy
                        </>
                    )}
                </Button>
            </div>

            {/* Markdown content */}
            <div className="flex-1 overflow-y-auto p-4 bg-white">
                <div className="prose prose-sm max-w-none prose-headings:text-gray-900 prose-p:text-gray-700 prose-a:text-primary-600 prose-code:text-primary-600 prose-pre:bg-gray-50">
                    <ReactMarkdown rehypePlugins={[rehypeHighlight]}>
                        {content}
                    </ReactMarkdown>
                </div>
            </div>
        </div>
    );
};
