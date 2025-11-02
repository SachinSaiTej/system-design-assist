"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface DesignHistory {
  id: string;
  design: string;
  timestamp: Date;
  instruction?: string;
}

export interface DesignState {
  currentDesign: string;
  history: DesignHistory[];
  sessionId: string | null;
  activeSection: string | null;
  isLoading: boolean;
  setCurrentDesign: (design: string) => void;
  addToHistory: (design: string, instruction?: string) => void;
  setSessionId: (sessionId: string) => void;
  setActiveSection: (section: string | null) => void;
  setIsLoading: (loading: boolean) => void;
  clearHistory: () => void;
  restoreFromHistory: (historyId: string) => void;
}

const generateHistoryId = () => {
  return `hist-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
};

export const useDesignStore = create<DesignState>()(
  persist(
    (set) => ({
      currentDesign: "",
      history: [],
      sessionId: null,
      activeSection: null,
      isLoading: false,

      setCurrentDesign: (design: string) => {
        set({ currentDesign: design });
      },

      addToHistory: (design: string, instruction?: string) => {
        set((state) => ({
          history: [
            {
              id: generateHistoryId(),
              design,
              timestamp: new Date(),
              instruction,
            },
            ...state.history,
          ].slice(0, 50), // Keep last 50 versions
        }));
      },

      setSessionId: (sessionId: string) => {
        set({ sessionId });
      },

      setActiveSection: (section: string | null) => {
        set({ activeSection: section });
      },

      setIsLoading: (loading: boolean) => {
        set({ isLoading: loading });
      },

      clearHistory: () => {
        set({ history: [] });
      },

      restoreFromHistory: (historyId: string) => {
        set((state) => {
          const historyItem = state.history.find((h) => h.id === historyId);
          if (historyItem) {
            return {
              currentDesign: historyItem.design,
            };
          }
          return state;
        });
      },
    }),
    {
      name: "design-storage",
      // Custom serialization for Date objects
      partialize: (state) => ({
        currentDesign: state.currentDesign,
        history: state.history.map((h) => ({
          ...h,
          timestamp: h.timestamp.toISOString(),
        })),
        sessionId: state.sessionId,
        activeSection: state.activeSection,
      }),
      // Custom deserialization for Date objects
      onRehydrateStorage: () => (state) => {
        if (state && state.history) {
          state.history = state.history.map((h: any) => ({
            ...h,
            timestamp:
              h.timestamp instanceof Date
                ? h.timestamp
                : new Date(h.timestamp as string),
          }));
        }
      },
    }
  )
);

