"use client";

import { useState, useMemo, memo } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import "highlight.js/styles/github-dark.css";
import MermaidRenderer from "./MermaidRenderer";

interface MarkdownRendererProps {
  content: string;
}

// Memoize the markdown content component to prevent re-renders when only debug state changes
const MarkdownContent = memo(function MarkdownContent({ content }: { content: string }) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      rehypePlugins={[rehypeHighlight]}
      components={{
        // Style code blocks with Mermaid support
        code({ node, inline, className, children, ...props }: any) {
          const match = /language-(\w+)/.exec(className || "");
          const language = match ? match[1] : "";
          
          // Extract code content properly
          const codeContent = Array.isArray(children)
            ? children.join("")
            : String(children);
          const codeString = codeContent.replace(/\n$/, "").trim();

          if (!inline && language === "mermaid" && codeString) {
            // Generate a stable key based on chart content to prevent unnecessary re-renders
            let keyHash = 0;
            for (let i = 0; i < codeString.length; i++) {
              keyHash = ((keyHash << 5) - keyHash) + codeString.charCodeAt(i);
              keyHash = keyHash & keyHash;
            }
            const stableKey = `mermaid-${Math.abs(keyHash).toString(36)}`;
            
            return <MermaidRenderer key={stableKey} chart={codeString} id={stableKey} />;
          }

          if (!inline && match) {
            return (
              <pre className="bg-gray-100 dark:bg-gray-800 rounded-lg p-4 overflow-x-auto">
                <code className={className} {...props}>
                  {children}
                </code>
              </pre>
            );
          }

          return (
            <code
              className="bg-gray-100 dark:bg-gray-800 px-1.5 py-0.5 rounded text-sm"
              {...props}
            >
              {children}
            </code>
          );
        },
        // Style headings
        h1: ({ children }) => (
          <h1 className="text-3xl font-bold mt-8 mb-4 text-gray-900 dark:text-gray-100">
            {children}
          </h1>
        ),
        h2: ({ children }) => (
          <h2 className="text-2xl font-semibold mt-6 mb-3 text-gray-800 dark:text-gray-200">
            {children}
          </h2>
        ),
        h3: ({ children }) => (
          <h3 className="text-xl font-semibold mt-4 mb-2 text-gray-700 dark:text-gray-300">
            {children}
          </h3>
        ),
        // Style lists
        ul: ({ children }) => (
          <ul className="list-disc list-inside space-y-2 my-4">
            {children}
          </ul>
        ),
        ol: ({ children }) => (
          <ol className="list-decimal list-inside space-y-2 my-4">
            {children}
          </ol>
        ),
        // Style paragraphs
        p: ({ children }) => (
          <p className="mb-4 text-gray-700 dark:text-gray-300 leading-relaxed">
            {children}
          </p>
        ),
        // Style blockquotes
        blockquote: ({ children }) => (
          <blockquote className="border-l-4 border-blue-500 pl-4 italic my-4 text-gray-600 dark:text-gray-400">
            {children}
          </blockquote>
        ),
      }}
    >
      {content}
    </ReactMarkdown>
  );
});

export default function MarkdownRenderer({ content }: MarkdownRendererProps) {
  const [showDebug, setShowDebug] = useState(false);
  
  // Memoize mermaidBlocks check so it doesn't recalculate on every render
  const mermaidBlocks = useMemo(() => content.match(/```mermaid\n([\s\S]*?)```/g), [content]);
  const hasMermaid = mermaidBlocks && mermaidBlocks.length > 0;

  return (
    <div className="prose prose-lg max-w-none dark:prose-invert">
      {/* Debug Panel */}
      <div className="mb-4 p-3 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className={`text-sm font-medium ${hasMermaid ? 'text-green-600 dark:text-green-400' : 'text-orange-600 dark:text-orange-400'}`}>
              {hasMermaid 
                ? `✓ Found ${mermaidBlocks?.length || 0} Mermaid diagram(s)` 
                : '⚠ No Mermaid diagrams found in response'}
            </span>
            <button
              onClick={() => setShowDebug(!showDebug)}
              className="text-xs text-blue-600 dark:text-blue-400 hover:underline"
            >
              {showDebug ? 'Hide' : 'Show'} Debug Info
            </button>
          </div>
        </div>
        {showDebug && (
          <div className="mt-3 text-xs">
            <p className="font-semibold mb-1">Mermaid blocks found:</p>
            {mermaidBlocks ? (
              <ul className="list-disc list-inside space-y-1 text-gray-700 dark:text-gray-300">
                {mermaidBlocks.map((block, idx) => (
                  <li key={idx}>
                    Block {idx + 1}: {block.substring(0, 100)}...
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-600 dark:text-gray-400">
                Search pattern: <code className="bg-gray-200 dark:bg-gray-700 px-1 rounded">```mermaid</code>
              </p>
            )}
            <details className="mt-2">
              <summary className="cursor-pointer text-blue-600 dark:text-blue-400">View raw content (first 500 chars)</summary>
              <pre className="mt-2 p-2 bg-gray-100 dark:bg-gray-800 rounded text-xs overflow-x-auto">
                {content.substring(0, 500)}...
              </pre>
            </details>
          </div>
        )}
      </div>
      
      {/* Memoized content - won't re-render when showDebug changes */}
      <MarkdownContent content={content} />
    </div>
  );
}
