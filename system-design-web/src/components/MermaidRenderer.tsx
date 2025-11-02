"use client";

import { useEffect, useRef, useState, useMemo } from "react";
import mermaid from "mermaid";

interface MermaidRendererProps {
  chart: string;
  id?: string;
}

// Initialize Mermaid once globally
let mermaidInitialized = false;

const initializeMermaid = () => {
  if (!mermaidInitialized && typeof window !== "undefined") {
    mermaid.initialize({
      startOnLoad: false,
      theme: "default",
      securityLevel: "loose",
      flowchart: {
        useMaxWidth: true,
        htmlLabels: true,
      },
    });
    mermaidInitialized = true;
  }
};

/**
 * Preprocess Mermaid chart to fix common syntax issues
 * - Escapes parentheses in node labels that aren't part of shape syntax
 * - Fixes quotes in labels
 */
const preprocessMermaidChart = (chart: string): string => {
  let processed = chart.trim();
  
  // Pattern to match node definitions: A[Label] or A["Label"] or A(Label) or A((Label))
  // We need to escape parentheses in square brackets (flowchart nodes)
  // but preserve parentheses that define node shapes like (round) or ((stadium))
  
  // Fix parentheses inside square brackets - replace ( with &#40; and ) with &#41;
  processed = processed.replace(/\[([^\]]*\([^)]*\)[^\]]*)\]/g, (match, label) => {
    // Check if this is actually a shape syntax like (()) or () not a label
    // If the whole thing is just parentheses, it's likely shape syntax
    if (/^[()]+$/.test(label.trim())) {
      return match;
    }
    // Otherwise, escape parentheses in the label
    const escaped = label
      .replace(/\(/g, '&#40;')
      .replace(/\)/g, '&#41;');
    return `[${escaped}]`;
  });
  
  // Also handle parentheses in quoted labels: A["Label (with parens)"]
  processed = processed.replace(/"([^"]*\([^)]*\)[^"]*)"/g, (match, label) => {
    const escaped = label
      .replace(/\(/g, '&#40;')
      .replace(/\)/g, '&#41;');
    return `"${escaped}"`;
  });
  
  return processed;
};

// Global cache to persist rendered SVGs across all MermaidRenderer instances
const mermaidCache = new Map<string, string>();

// Track render instances to ensure uniqueness even with hash collisions
let renderInstanceCounter = 0;

export default function MermaidRenderer({ chart, id }: MermaidRendererProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  
  // Create a unique instance ID for this renderer instance (persists across re-renders)
  const instanceIdRef = useRef<string>(`instance-${renderInstanceCounter++}`);
  
  // Preprocess chart first (for display) but use original for ID calculation
  // This ensures cache keys are stable even if preprocessing changes
  const preprocessedChart = useMemo(() => {
    return preprocessMermaidChart(chart.trim());
  }, [chart]);
  
  // Generate a stable ID based on ORIGINAL chart content (not preprocessed)
  // This ensures cache consistency - same original chart = same ID
  // DON'T include instance ID here - we want same charts to share cache
  const chartId = useMemo(() => {
    if (id) return id;
    // Generate a stable ID based only on original chart content hash
    let hash = 0;
    const chartStr = chart.trim();
    for (let i = 0; i < chartStr.length; i++) {
      const char = chartStr.charCodeAt(i);
      hash = (hash << 5) - hash + char;
      hash = hash & hash; // Convert to 32bit integer
    }
    return `mermaid-${Math.abs(hash).toString(36)}`;
  }, [chart, id]);
  
  // Separate ID for Mermaid's render function - must be unique per render instance
  const mermaidRenderId = useMemo(() => {
    return `${chartId}-${instanceIdRef.current}`;
  }, [chartId]);
  
  // Initialize state - check cache immediately on mount
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(() => {
    // Check cache on initial state setup
    return !mermaidCache.has(chartId);
  });
  const [svgContent, setSvgContent] = useState<string | null>(() => {
    // Restore from cache on mount if available
    return mermaidCache.get(chartId) || null;
  });

  useEffect(() => {
    if (!chart || !chart.trim()) {
      setIsLoading(false);
      return;
    }

    // CRITICAL: Check global cache first - if we've rendered this chartId before, restore immediately
    // This prevents re-rendering when parent component re-renders (e.g., debug toggle)
    // Also handles React Strict Mode double-invoke
    const cachedSvg = mermaidCache.get(chartId);
    if (cachedSvg) {
      console.log(`[MermaidRenderer] Restoring from global cache for ${chartId} (instance: ${instanceIdRef.current})`);
      // Use setTimeout to ensure this happens after any DOM clearing from strict mode
      setTimeout(() => {
        setSvgContent(cachedSvg);
        setIsLoading(false);
        
        // Force update the DOM if the container exists but doesn't have the SVG
        if (containerRef.current && !containerRef.current.querySelector('svg')) {
          containerRef.current.innerHTML = cachedSvg;
          console.log(`[MermaidRenderer] Force-injected SVG into DOM for ${chartId}`);
        }
      }, 0);
      return;
    }

    // Initialize Mermaid globally if not already done
    initializeMermaid();

    setIsLoading(true);
    setError(null);
    setSvgContent(null);

    // Render the chart
    const renderChart = async () => {
      try {
        // Use preprocessed chart for rendering
        const chartToRender = preprocessedChart;
        
        console.log(`[MermaidRenderer] Starting render for chartId: ${chartId}`, {
          chartId,
          chartLength: chartToRender.length,
          chartPreview: chartToRender.substring(0, 50),
          originalLength: chart.trim().length,
          isFromCache: !!mermaidCache.get(chartId)
        });

        // Use unique mermaidRenderId for Mermaid's internal tracking
        // This prevents conflicts when multiple diagrams render simultaneously
        const result = await mermaid.render(mermaidRenderId, chartToRender);
        console.log(`[MermaidRenderer] Render complete for ${chartId}`, {
          chartId,
          instanceId: instanceIdRef.current,
          mermaidRenderId,
          svgLength: result.svg.length,
          bindFunctions: typeof result.bindFunctions,
          cacheSize: mermaidCache.size
        });

        // Store SVG content in global cache and state for persistence across re-renders
        // Use chartId (without -render suffix) as cache key for consistency
        mermaidCache.set(chartId, result.svg);
        
        // Set state and force DOM update to handle React Strict Mode double-invoke
        setSvgContent(result.svg);
        setIsLoading(false);
        
        // Immediately inject into DOM if container exists (handles strict mode)
        if (containerRef.current) {
          containerRef.current.innerHTML = result.svg;
        }
        
        console.log(`[MermaidRenderer] Cached SVG for ${chartId} (instance: ${instanceIdRef.current}), total cached: ${mermaidCache.size}`);
        
        // After state update and re-render completes, bind functions if needed
        // Use multiple frame delays to ensure DOM has fully updated (React strict mode double-invoke)
        requestAnimationFrame(() => {
          requestAnimationFrame(() => {
            setTimeout(() => {
              // Try to find container by instance ID first (more specific)
              const containerByInstance = document.querySelector(`[data-instance-id="${instanceIdRef.current}"]`);
              const containerByAttr = document.querySelector(`[data-mermaid-id="${chartId}"]`);
              const container = containerByInstance || containerByAttr || containerRef.current;
              
              if (container) {
                let insertedSvg = container.querySelector('svg');
                
                // If SVG not found, force inject it (handles strict mode clearing)
                if (!insertedSvg && mermaidCache.has(chartId)) {
                  const cached = mermaidCache.get(chartId)!;
                  container.innerHTML = cached;
                  insertedSvg = container.querySelector('svg');
                  console.log(`[MermaidRenderer] Re-injected SVG for ${chartId} (instance: ${instanceIdRef.current}) due to strict mode`);
                }
                
                if (insertedSvg) {
                  console.log(`[MermaidRenderer] SVG successfully verified in DOM for ${chartId} (instance: ${instanceIdRef.current})`, {
                    svgWidth: insertedSvg.getAttribute('width'),
                    svgHeight: insertedSvg.getAttribute('height'),
                    svgViewBox: insertedSvg.getAttribute('viewBox'),
                    method: containerByInstance ? 'instance-id' : containerByAttr ? 'data-attr' : 'ref'
                  });
                  
                  // Call bindFunctions if available (for interactive elements)
                  if (result.bindFunctions && typeof result.bindFunctions === 'function') {
                    result.bindFunctions(container as HTMLElement);
                  }
                } else {
                  console.warn(`[MermaidRenderer] SVG still not in DOM for ${chartId} (instance: ${instanceIdRef.current}) after re-injection attempt`);
                }
              } else {
                console.warn(`[MermaidRenderer] Container not found for ${chartId} (instance: ${instanceIdRef.current})`);
              }
            }, 100);
          });
        });
      } catch (err: any) {
        console.error(`[MermaidRenderer] Error rendering ${chartId}:`, err);
        
        // Extract more detailed error information
        let errorMessage = "Failed to render diagram";
        if (err instanceof Error) {
          errorMessage = err.message;
        } else if (err?.message) {
          errorMessage = err.message;
        } else if (typeof err === 'string') {
          errorMessage = err;
        }
        
        // If it's a parse error, include the problematic code
        if (errorMessage.includes('Parse error') || errorMessage.includes('parse')) {
          errorMessage = `${errorMessage}\n\nDiagram code:\n${preprocessedChart.substring(0, 200)}${preprocessedChart.length > 200 ? '...' : ''}`;
        }
        
        setError(errorMessage);
        setIsLoading(false);
      }
    };

    renderChart();
  }, [chart, chartId, preprocessedChart]);

  if (error) {
    return (
      <div className="my-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
        <p className="text-sm font-semibold text-red-600 dark:text-red-400 mb-2">
          ⚠️ Diagram Rendering Error
        </p>
        <p className="text-sm text-red-600 dark:text-red-400 mb-3 whitespace-pre-wrap">
          {error}
        </p>
        <details className="mt-3">
          <summary className="text-xs text-red-500 dark:text-red-400 cursor-pointer hover:underline">
            View raw Mermaid code
          </summary>
          <pre className="mt-2 p-2 bg-red-100 dark:bg-red-900/30 rounded text-xs text-red-700 dark:text-red-300 overflow-x-auto">
            {chart}
          </pre>
        </details>
        <p className="text-xs text-red-600 dark:text-red-400 mt-3">
          💡 Tip: This might be due to special characters in node labels. Try refining the design to simplify diagram labels.
        </p>
      </div>
    );
  }

  // Use rendered SVG from cache if state is cleared
  const displaySvg = svgContent || mermaidCache.get(chartId) || null;

  if (isLoading || !displaySvg) {
    return (
      <div className="my-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
        <p className="text-sm text-gray-600 dark:text-gray-400">
          {isLoading ? "Rendering diagram..." : "Preparing diagram..."}
        </p>
      </div>
    );
  }

  return (
    <div className="my-4 mermaid-container-wrapper bg-white dark:bg-gray-900 rounded-lg p-4 overflow-x-auto">
      <div
        ref={containerRef}
        data-mermaid-id={chartId}
        data-instance-id={instanceIdRef.current}
        className="flex justify-center items-center mermaid-diagram"
        dangerouslySetInnerHTML={displaySvg ? { __html: displaySvg } : undefined}
      />
    </div>
  );
}

