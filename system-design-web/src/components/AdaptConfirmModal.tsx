"use client";

import { useState } from "react";
import { ReferenceHighlight } from "./ReferencePanel";

interface AdaptConfirmModalProps {
  reference: ReferenceHighlight;
  onConfirm: (constraints?: string) => void;
  onCancel: () => void;
}

export default function AdaptConfirmModal({
  reference,
  onConfirm,
  onCancel,
}: AdaptConfirmModalProps) {
  const [constraints, setConstraints] = useState("");

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
            Adapt Reference Design
          </h2>

          <div className="mb-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
              {reference.title}
            </h3>
            <a
              href={reference.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-blue-600 dark:text-blue-400 hover:underline break-all"
            >
              {reference.url}
            </a>
          </div>

          <div className="mb-6">
            <label
              htmlFor="constraints"
              className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
            >
              Additional Constraints or Modifications (Optional)
            </label>
            <textarea
              id="constraints"
              value={constraints}
              onChange={(e) => setConstraints(e.target.value)}
              placeholder="E.g., Must use AWS services, should handle 10M users, add Redis caching..."
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg 
                       focus:ring-2 focus:ring-blue-500 focus:border-transparent 
                       dark:bg-gray-700 dark:text-white
                       resize-none"
              rows={4}
            />
            <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
              Specify any additional requirements or modifications you want applied to this reference design.
            </p>
          </div>

          <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4 mb-6">
            <p className="text-sm text-yellow-800 dark:text-yellow-300">
              <strong>Note:</strong> The adapted design will be based on the ByteByteGo framework and will include
              a "Sources" section and a "Changes vs Source" summary.
            </p>
          </div>

          <div className="flex gap-3 justify-end">
            <button
              onClick={onCancel}
              className="px-6 py-2 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 
                       text-gray-700 dark:text-gray-300 font-medium rounded-lg transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={() => onConfirm(constraints.trim() || undefined)}
              className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors"
            >
              Confirm & Adapt
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

