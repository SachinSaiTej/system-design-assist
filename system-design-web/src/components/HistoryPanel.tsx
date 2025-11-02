"use client";

import { useDesignStore } from "@/store/designStore";

export default function HistoryPanel() {
  const { history, restoreFromHistory, clearHistory, currentDesign } =
    useDesignStore();

  const formatTimestamp = (date: Date) => {
    return new Intl.DateTimeFormat("en-US", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }).format(date);
  };

  if (history.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
          Design History
        </h3>
        <p className="text-sm text-gray-600 dark:text-gray-400">
          No previous versions yet. Refinements will appear here.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
      <div className="p-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Design History
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            {history.length} previous {history.length === 1 ? "version" : "versions"}
          </p>
        </div>
        {history.length > 0 && (
          <button
            onClick={clearHistory}
            className="px-3 py-1.5 text-sm text-red-600 hover:text-red-700 
                     hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors
                     focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
          >
            Clear
          </button>
        )}
      </div>
      <div className="divide-y divide-gray-200 dark:divide-gray-700 max-h-[400px] overflow-y-auto">
        {history.map((item) => {
          const isCurrentVersion =
            item.design === currentDesign;
          return (
            <div
              key={item.id}
              className={`p-4 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors ${
                isCurrentVersion ? "bg-blue-50 dark:bg-blue-900/20" : ""
              }`}
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium text-gray-900 dark:text-white">
                      {formatTimestamp(item.timestamp)}
                    </span>
                    {isCurrentVersion && (
                      <span className="px-2 py-0.5 text-xs font-medium bg-blue-600 text-white rounded">
                        Current
                      </span>
                    )}
                  </div>
                  {item.instruction && (
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                      "{item.instruction}"
                    </p>
                  )}
                  <p className="text-xs text-gray-500 dark:text-gray-500 mt-2">
                    {item.design.length} characters
                  </p>
                </div>
                {!isCurrentVersion && (
                  <button
                    onClick={() => restoreFromHistory(item.id)}
                    className="px-3 py-1.5 text-sm bg-blue-600 hover:bg-blue-700 text-white 
                             rounded-lg transition-colors focus:outline-none focus:ring-2 
                             focus:ring-blue-500 focus:ring-offset-2 whitespace-nowrap"
                  >
                    Restore
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

