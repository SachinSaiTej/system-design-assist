"use client";

import { useState, useEffect } from "react";
import axios from "axios";
import { useDesignStore } from "@/store/designStore";
import LoadingSpinner from "./LoadingSpinner";

interface Section {
  name: string;
  level: number;
  startIndex: number;
  endIndex: number;
}

interface SectionViewerProps {
  onSectionRegenerated?: () => void;
}

export default function SectionViewer({
  onSectionRegenerated,
}: SectionViewerProps) {
  const [sections, setSections] = useState<Section[]>([]);
  const [regeneratingSection, setRegeneratingSection] = useState<
    string | null
  >(null);
  const [instruction, setInstruction] = useState<{ [key: string]: string }>(
    {}
  );

  const {
    currentDesign,
    sessionId,
    setCurrentDesign,
    addToHistory,
    setSessionId,
    setIsLoading: setStoreLoading,
  } = useDesignStore();

  useEffect(() => {
    if (currentDesign) {
      const extractedSections = extractSections(currentDesign);
      setSections(extractedSections);
    }
  }, [currentDesign]);

  const extractSections = (markdown: string): Section[] => {
    const lines = markdown.split("\n");
    const sections: Section[] = [];
    const sectionStack: Section[] = [];

    lines.forEach((line, index) => {
      if (line.trim().startsWith("#")) {
        const level = line.match(/^#+/)?.length || 0;
        const name = line.replace(/^#+\s*/, "").trim();

        // Pop sections with higher or equal level
        while (
          sectionStack.length > 0 &&
          sectionStack[sectionStack.length - 1].level >= level
        ) {
          const prevSection = sectionStack.pop()!;
          prevSection.endIndex = index;
        }

        const section: Section = {
          name,
          level,
          startIndex: index,
          endIndex: lines.length, // Will be updated when next section is found
        };

        sections.push(section);
        sectionStack.push(section);
      }
    });

    return sections.filter((s) => s.level <= 2); // Only show h1 and h2
  };

  const handleRegenerate = async (sectionName: string) => {
    if (!currentDesign) return;

    const userInstruction =
      instruction[sectionName] || "Improve and expand this section";
    setRegeneratingSection(sectionName);
    setStoreLoading(true);

    try {
      const response = await axios.post("http://localhost:8000/api/section", {
        previous_design: currentDesign,
        section_name: sectionName,
        instruction: userInstruction,
        session_id: sessionId,
      });

      const updatedDesign = response.data.updated_design;
      const newSessionId = response.data.session_id;

      // Update store
      setCurrentDesign(updatedDesign);
      addToHistory(updatedDesign, `Regenerated: ${sectionName}`);
      if (newSessionId) {
        setSessionId(newSessionId);
      }

      // Clear instruction for this section
      setInstruction((prev) => {
        const next = { ...prev };
        delete next[sectionName];
        return next;
      });

      onSectionRegenerated?.();
    } catch (error: any) {
      console.error("Section regeneration error:", error);
      alert(
        error.response?.data?.detail?.message ||
          error.message ||
          "Failed to regenerate section. Please try again."
      );
    } finally {
      setRegeneratingSection(null);
      setStoreLoading(false);
    }
  };

  if (!currentDesign) {
    return (
      <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
        <p className="text-sm text-gray-600 dark:text-gray-400">
          No design available.
        </p>
      </div>
    );
  }

  if (sections.length === 0) {
    return (
      <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
        <p className="text-sm text-gray-600 dark:text-gray-400">
          No sections found in the design document.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
          Document Sections
        </h3>
        <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
          Regenerate individual sections with custom instructions
        </p>
      </div>
      <div className="divide-y divide-gray-200 dark:divide-gray-700">
        {sections.map((section, idx) => (
          <div key={idx} className="p-4 hover:bg-gray-50 dark:hover:bg-gray-700">
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1">
                <h4
                  className={`font-medium text-gray-900 dark:text-white ${
                    section.level === 1 ? "text-lg" : "text-base"
                  }`}
                >
                  {section.name}
                </h4>
                <div className="mt-2">
                  <input
                    type="text"
                    value={instruction[section.name] || ""}
                    onChange={(e) =>
                      setInstruction({
                        ...instruction,
                        [section.name]: e.target.value,
                      })
                    }
                    placeholder="Optional: Custom instruction for this section..."
                    className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 
                             rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100
                             focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>
              <button
                onClick={() => handleRegenerate(section.name)}
                disabled={regeneratingSection === section.name}
                className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white text-sm font-medium
                         rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed
                         focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2
                         whitespace-nowrap"
              >
                {regeneratingSection === section.name ? (
                  <LoadingSpinner size="sm" />
                ) : (
                  "Regenerate"
                )}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

