"use client";
import { useSearchParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import MarkdownRenderer from "@/components/MarkdownRenderer";

export default function ResultPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [designMarkdown, setDesignMarkdown] = useState<string>("");

  useEffect(() => {
    const designParam = searchParams.get("design");
    if (designParam) {
      setDesignMarkdown(decodeURIComponent(designParam));
    } else {
      // Redirect to home if no design data
      router.push("/");
    }
  }, [searchParams, router]);

  const handleNewDesign = () => {
    router.push("/");
  };

  if (!designMarkdown) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-600 dark:text-gray-400">Loading...</p>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8 max-w-5xl">
        {/* Header */}
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
              System Design Document
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              Generated system design solution
            </p>
          </div>
          <button
            onClick={handleNewDesign}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold 
                     py-2 px-6 rounded-lg transition-colors
                     focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            New Design
          </button>
        </div>

        {/* Content */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-8 mb-8">
          <MarkdownRenderer content={designMarkdown} />
        </div>

        {/* Footer */}
        <div className="text-center text-sm text-gray-500 dark:text-gray-400 mb-8">
          <p>System Design Assistant • Phase 1 MVP</p>
        </div>
      </div>
    </main>
  );
}

