"use client";
import { useSearchParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import MarkdownRenderer from "@/components/MarkdownRenderer";
import ChatPanel from "@/components/ChatPanel";
import SectionViewer from "@/components/SectionViewer";
import HistoryPanel from "@/components/HistoryPanel";
import { useDesignStore } from "@/store/designStore";
import LoadingSpinner from "@/components/LoadingSpinner";

type TabType = "design" | "sections" | "history" | "chat";

export default function ResultPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<TabType>("design");
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const {
    currentDesign,
    setCurrentDesign,
    setSessionId,
    isLoading,
  } = useDesignStore();

  useEffect(() => {
    const designParam = searchParams.get("design");
    if (designParam) {
      // Next.js App Router automatically decodes query parameters,
      // but we'll handle cases where double-encoding might occur
      let designContent = designParam;
      
      // Only attempt to decode if the string contains encoded characters
      // This avoids errors when Next.js has already decoded it
      if (designParam.includes("%")) {
        try {
          designContent = decodeURIComponent(designParam);
        } catch (error) {
          // If decoding fails, use as-is (likely already decoded)
          designContent = designParam;
        }
      }
      
      setCurrentDesign(designContent);
      // Generate a session ID for this design
      setSessionId(`session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`);
    } else if (!currentDesign) {
      // Only redirect if we don't have a design in storage
      router.push("/");
    }
  }, [searchParams, router, setCurrentDesign, setSessionId, currentDesign]);

  const handleNewDesign = () => {
    router.push("/");
  };

  if (!currentDesign && !searchParams.get("design")) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <LoadingSpinner />
          <p className="text-gray-600 dark:text-gray-400 mt-4">Loading...</p>
        </div>
      </div>
    );
  }

  const tabs: Array<{ id: TabType; label: string; icon: string }> = [
    { id: "design", label: "Design", icon: "📄" },
    { id: "sections", label: "Sections", icon: "📑" },
    { id: "chat", label: "Refine", icon: "💬" },
    { id: "history", label: "History", icon: "🕒" },
  ];

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-6 max-w-7xl">
        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
              System Design Document
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              Interactive design refinement and iteration
            </p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="px-4 py-2 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 
                       text-gray-700 dark:text-gray-300 font-medium rounded-lg transition-colors
                       focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
            >
              {sidebarOpen ? "Hide" : "Show"} Sidebar
            </button>
            <button
              onClick={handleNewDesign}
              className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold 
                       rounded-lg transition-colors
                       focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              New Design
            </button>
          </div>
        </div>

        {/* Tabs */}
        <div className="mb-6 border-b border-gray-200 dark:border-gray-700">
          <div className="flex space-x-1">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-6 py-3 font-medium text-sm rounded-t-lg transition-colors
                  ${
                    activeTab === tab.id
                      ? "bg-white dark:bg-gray-800 text-blue-600 dark:text-blue-400 border-b-2 border-blue-600 dark:border-blue-400"
                      : "text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-800"
                  }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        <div className="flex gap-6">
          {/* Main Content Area */}
          <div
            className={`transition-all duration-300 ${
              sidebarOpen ? "flex-1" : "w-full"
            }`}
          >
            {activeTab === "design" && (
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-8">
                {isLoading && (
                  <div className="mb-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg flex items-center gap-3">
                    <LoadingSpinner size="sm" />
                    <span className="text-sm text-blue-600 dark:text-blue-400">
                      Updating design...
                    </span>
                  </div>
                )}
                <MarkdownRenderer content={currentDesign || ""} />
              </div>
            )}

            {activeTab === "sections" && (
              <SectionViewer
                onSectionRegenerated={() => {
                  // Scroll to top and switch to design view
                  window.scrollTo({ top: 0, behavior: "smooth" });
                  setTimeout(() => setActiveTab("design"), 300);
                }}
              />
            )}

            {activeTab === "chat" && (
              <div className="h-[600px]">
                <ChatPanel
                  onRefinementComplete={() => {
                    // Scroll to top and switch to design view
                    window.scrollTo({ top: 0, behavior: "smooth" });
                    setTimeout(() => setActiveTab("design"), 300);
                  }}
                />
              </div>
            )}

            {activeTab === "history" && <HistoryPanel />}
          </div>

          {/* Sidebar */}
          {sidebarOpen && (
            <div className="w-80 space-y-6">
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4 border border-gray-200 dark:border-gray-700">
                <h3 className="text-sm font-semibold text-gray-900 dark:text-white mb-3">
                  Quick Actions
                </h3>
                <div className="space-y-2">
                  <button
                    onClick={() => setActiveTab("chat")}
                    className="w-full px-4 py-2 text-left text-sm bg-blue-50 dark:bg-blue-900/20 
                             hover:bg-blue-100 dark:hover:bg-blue-900/30 text-blue-700 dark:text-blue-300 
                             rounded-lg transition-colors"
                  >
                    💬 Refine Design
                  </button>
                  <button
                    onClick={() => setActiveTab("sections")}
                    className="w-full px-4 py-2 text-left text-sm bg-green-50 dark:bg-green-900/20 
                             hover:bg-green-100 dark:hover:bg-green-900/30 text-green-700 dark:text-green-300 
                             rounded-lg transition-colors"
                  >
                    📑 Regenerate Section
                  </button>
                  <button
                    onClick={() => setActiveTab("history")}
                    className="w-full px-4 py-2 text-left text-sm bg-purple-50 dark:bg-purple-900/20 
                             hover:bg-purple-100 dark:hover:bg-purple-900/30 text-purple-700 dark:text-purple-300 
                             rounded-lg transition-colors"
                  >
                    🕒 View History
                  </button>
                </div>
              </div>

              {activeTab === "design" && (
                <div>
                  <ChatPanel
                    onRefinementComplete={() => {
                      setActiveTab("design");
                    }}
                  />
                </div>
              )}

              {activeTab !== "design" && (
                <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
                  <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                    <h3 className="text-sm font-semibold text-gray-900 dark:text-white">
                      Current Design
                    </h3>
                  </div>
                  <div className="p-4 max-h-[300px] overflow-y-auto">
                    <div className="prose prose-sm max-w-none dark:prose-invert">
                      <MarkdownRenderer
                        content={
                          currentDesign?.substring(0, 500) +
                          (currentDesign && currentDesign.length > 500
                            ? "..."
                            : "") || ""
                        }
                      />
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="text-center text-sm text-gray-500 dark:text-gray-400 mt-8 mb-4">
          <p>System Design Assistant • Phase 2 - Interactive Refinement</p>
        </div>
      </div>
    </main>
  );
}

