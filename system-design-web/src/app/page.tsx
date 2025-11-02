"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import LoadingSpinner from "@/components/LoadingSpinner";

const API_URL = "http://localhost:8000/api/design/generate";

export default function Home() {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!input.trim()) {
      setError("Please enter a system design requirement");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_input: input }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail?.message || "Failed to generate design");
      }

      const data = await response.json();
      
      // Navigate to result page with the markdown content
      router.push(`/result?design=${encodeURIComponent(data.design_markdown)}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-16 max-w-4xl">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-4">
            System Design Assistant
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300">
            Describe your system requirements and get a comprehensive design document
          </p>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label 
                htmlFor="system-input" 
                className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
              >
                System Design Requirements
              </label>
              <textarea
                id="system-input"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="E.g., Design a URL shortener service like bit.ly that can handle 100 million URLs per day..."
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg 
                         focus:ring-2 focus:ring-blue-500 focus:border-transparent 
                         dark:bg-gray-700 dark:text-white
                         resize-none"
                rows={8}
                disabled={loading}
              />
              <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
                Be as specific as possible about your requirements, scale, and constraints
              </p>
            </div>

            {error && (
              <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 
                            rounded-lg p-4 text-red-800 dark:text-red-200">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 
                       text-white font-semibold py-3 px-6 rounded-lg transition-colors
                       focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              {loading ? "Generating..." : "Generate System Design"}
            </button>
          </form>

          {loading && (
            <div className="mt-8">
              <LoadingSpinner />
            </div>
          )}
        </div>

        <div className="mt-8 text-center text-sm text-gray-500 dark:text-gray-400">
          <p>Powered by AI • Phase 1 MVP</p>
        </div>
      </div>
    </main>
  );
}
