"use client";

import { useState, useRef, useEffect } from "react";
import axios from "axios";
import { useDesignStore } from "@/store/designStore";
import LoadingSpinner from "./LoadingSpinner";

interface ChatPanelProps {
  onRefinementComplete?: () => void;
}

export default function ChatPanel({ onRefinementComplete }: ChatPanelProps) {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<
    Array<{ role: "user" | "assistant"; content: string }>
  >([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const {
    currentDesign,
    sessionId,
    setCurrentDesign,
    addToHistory,
    setSessionId,
    setIsLoading: setStoreLoading,
  } = useDesignStore();

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim() || isLoading || !currentDesign) return;

    const userMessage = message.trim();
    setMessage("");
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setIsLoading(true);
    setStoreLoading(true);

    try {
      const response = await axios.post("http://localhost:8000/api/refine", {
        previous_design: currentDesign,
        instruction: userMessage,
        session_id: sessionId,
      });

      const refinedDesign = response.data.refined_design;
      const newSessionId = response.data.session_id;

      // Update store
      setCurrentDesign(refinedDesign);
      addToHistory(refinedDesign, userMessage);
      if (newSessionId) {
        setSessionId(newSessionId);
      }

      // Add assistant message
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Design has been refined based on your instructions.",
        },
      ]);

      onRefinementComplete?.();
    } catch (error: any) {
      console.error("Refinement error:", error);
      const errorMessage =
        error.response?.data?.detail?.message ||
        error.message ||
        "Failed to refine design. Please try again.";

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `Error: ${errorMessage}`,
        },
      ]);
    } finally {
      setIsLoading(false);
      setStoreLoading(false);
      textareaRef.current?.focus();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as any);
    }
  };

  if (!currentDesign) {
    return (
      <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
        <p className="text-sm text-gray-600 dark:text-gray-400">
          No design available. Please generate a design first.
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 min-h-[200px] max-h-[400px]">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 dark:text-gray-400 py-8">
            <p className="text-sm">
              Enter instructions to refine your design document.
            </p>
            <p className="text-xs mt-2">
              Examples: "Add caching layer", "Improve scalability section",
              "Add more details to architecture"
            </p>
          </div>
        )}
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-[80%] rounded-lg px-4 py-2 ${
                msg.role === "user"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100"
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 dark:bg-gray-700 rounded-lg px-4 py-2">
              <LoadingSpinner size="sm" />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="border-t border-gray-200 dark:border-gray-700 p-4">
        <div className="flex gap-2">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Enter refinement instructions..."
            disabled={isLoading}
            rows={2}
            className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg 
                     bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100
                     focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
                     disabled:opacity-50 disabled:cursor-not-allowed resize-none"
          />
          <button
            type="submit"
            disabled={!message.trim() || isLoading}
            className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold 
                     rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed
                     focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            {isLoading ? "Refining..." : "Refine"}
          </button>
        </div>
        <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
          Press Enter to submit, Shift+Enter for new line
        </p>
      </form>
    </div>
  );
}

