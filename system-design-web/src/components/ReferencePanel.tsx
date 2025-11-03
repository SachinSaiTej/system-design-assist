"use client";

import { useState } from "react";
import AdaptConfirmModal from "./AdaptConfirmModal";

export interface ReferenceHighlight {
  title: string;
  url: string;
  highlights: string[];
  assumptions: string[];
  components: string[];
  confidence_score: number;
  snippet?: string;
}

interface ReferencePanelProps {
  references: ReferenceHighlight[];
  onAdapt: (reference: ReferenceHighlight, constraints?: string) => void;
  onGenerateFresh: () => void;
  isLoading?: boolean;
}

export default function ReferencePanel({
  references,
  onAdapt,
  onGenerateFresh,
  isLoading = false,
}: ReferencePanelProps) {
  const [selectedReference, setSelectedReference] = useState<ReferenceHighlight | null>(null);
  const [showAdaptModal, setShowAdaptModal] = useState(false);

  const handleAdaptClick = (reference: ReferenceHighlight) => {
    setSelectedReference(reference);
    setShowAdaptModal(true);
  };

  const handleAdaptConfirm = (constraints?: string) => {
    if (selectedReference) {
      onAdapt(selectedReference, constraints);
    }
    setShowAdaptModal(false);
    setSelectedReference(null);
  };

  const getConfidenceColor = (score: number) => {
    if (score >= 0.7) return "text-green-600 dark:text-green-400";
    if (score >= 0.4) return "text-yellow-600 dark:text-yellow-400";
    return "text-red-600 dark:text-red-400";
  };

  const getConfidenceLabel = (score: number) => {
    if (score >= 0.7) return "High";
    if (score >= 0.4) return "Medium";
    return "Low";
  };

  if (isLoading) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-8">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="mt-4 text-gray-600 dark:text-gray-400">
            Searching for references...
          </p>
        </div>
      </div>
    );
  }

  if (references.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-8">
        <div className="text-center">
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            No references found. You can generate a fresh design.
          </p>
          <button
            onClick={onGenerateFresh}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-colors"
          >
            Generate Fresh Design
          </button>
        </div>
      </div>
    );
  }

  return (
    <>
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-8">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            Found {references.length} Reference{references.length !== 1 ? "s" : ""}
          </h2>
          <p className="text-gray-600 dark:text-gray-400">
            Choose a reference to adapt or generate a fresh design
          </p>
        </div>

        <div className="space-y-6 mb-6">
          {references.map((ref, index) => (
            <div
              key={index}
              className="border border-gray-200 dark:border-gray-700 rounded-lg p-6 hover:border-blue-300 dark:hover:border-blue-600 transition-colors"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    {ref.title}
                  </h3>
                  <a
                    href={ref.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-blue-600 dark:text-blue-400 hover:underline break-all"
                  >
                    {ref.url}
                  </a>
                </div>
                <div className="ml-4 text-right">
                  <div className={`text-sm font-semibold ${getConfidenceColor(ref.confidence_score)}`}>
                    {getConfidenceLabel(ref.confidence_score)} Confidence
                  </div>
                  <div className="text-xs text-gray-500 dark:text-gray-400">
                    {(ref.confidence_score * 100).toFixed(0)}%
                  </div>
                </div>
              </div>

              {ref.snippet && (
                <div className="mb-4 p-3 bg-gray-50 dark:bg-gray-700 rounded text-sm text-gray-700 dark:text-gray-300">
                  {ref.snippet}
                </div>
              )}

              <div className="mb-4">
                <h4 className="text-sm font-semibold text-gray-900 dark:text-white mb-2">
                  Key Highlights:
                </h4>
                <ul className="list-disc list-inside space-y-1 text-sm text-gray-600 dark:text-gray-400">
                  {ref.highlights.map((highlight, idx) => (
                    <li key={idx}>{highlight || "No highlight available"}</li>
                  ))}
                </ul>
              </div>

              {ref.components.length > 0 && (
                <div className="mb-4">
                  <h4 className="text-sm font-semibold text-gray-900 dark:text-white mb-2">
                    Components:
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {ref.components.map((component, idx) => (
                      <span
                        key={idx}
                        className="px-2 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded text-xs"
                      >
                        {component}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {ref.assumptions.length > 0 && (
                <div className="mb-4">
                  <h4 className="text-sm font-semibold text-gray-900 dark:text-white mb-2">
                    Assumptions:
                  </h4>
                  <ul className="list-disc list-inside space-y-1 text-sm text-gray-600 dark:text-gray-400">
                    {ref.assumptions.map((assumption, idx) => (
                      <li key={idx}>{assumption}</li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="flex gap-3 mt-4">
                <button
                  onClick={() => handleAdaptClick(ref)}
                  className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors"
                >
                  Adapt This Design
                </button>
                <a
                  href={ref.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-4 py-2 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 font-medium rounded-lg transition-colors"
                >
                  View Original
                </a>
              </div>
            </div>
          ))}
        </div>

        <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
          <button
            onClick={onGenerateFresh}
            className="w-full px-6 py-3 bg-gray-600 hover:bg-gray-700 text-white font-semibold rounded-lg transition-colors"
          >
            Generate Fresh Design (Skip References)
          </button>
        </div>
      </div>

      {showAdaptModal && selectedReference && (
        <AdaptConfirmModal
          reference={selectedReference}
          onConfirm={handleAdaptConfirm}
          onCancel={() => {
            setShowAdaptModal(false);
            setSelectedReference(null);
          }}
        />
      )}
    </>
  );
}

