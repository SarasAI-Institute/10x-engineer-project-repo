import { PromptCard } from './PromptCard';
import { LoadingSpinner } from '../shared/LoadingSpinner';
import { ErrorMessage } from '../shared/ErrorMessage';

/**
 * Renders the main grid of prompt cards with loading, error, and empty states.
 *
 * State priority:
 * 1. **Loading** — shows a large centred `LoadingSpinner`.
 * 2. **Error** — shows an `ErrorMessage` with a retry button.
 * 3. **Empty (filtered)** — "No results found" message when search/collection
 *    filters are active but produced no results.
 * 4. **Empty (unfiltered)** — "No prompts yet" onboarding message.
 * 5. **Populated** — a responsive CSS grid of `PromptCard` components.
 *
 * @param {Object} props - Component props.
 * @param {Array<Object>} props.prompts - Array of prompt objects to render.
 * @param {Array<{id: string, name: string}>} props.collections - Full collections list,
 *   used to resolve collection names for each card badge.
 * @param {boolean} props.loading - When true renders the loading spinner.
 * @param {string} [props.error] - Error message string; when truthy renders an error state.
 * @param {function(): void} props.onRetry - Callback passed to `ErrorMessage` for the retry button.
 * @param {function(prompt: Object): void} props.onView - Called when a card is clicked to open detail view.
 * @param {function(prompt: Object): void} props.onEdit - Called when the edit icon on a card is clicked.
 * @param {function(prompt: Object): void} props.onDelete - Called when the delete icon on a card is clicked.
 * @param {boolean} props.isFiltered - When true and the list is empty, shows the "no results" empty
 *   state instead of the "no prompts yet" onboarding state.
 * @returns {JSX.Element} A loading spinner, error, empty state, or grid of prompt cards.
 *
 * @example
 * <PromptList
 *   prompts={prompts}
 *   collections={collections}
 *   loading={loadingPrompts}
 *   error={promptsError}
 *   onRetry={fetchPrompts}
 *   onView={setViewingPrompt}
 *   onEdit={openEdit}
 *   onDelete={handleDeletePrompt}
 *   isFiltered={Boolean(search || selectedCollection)}
 * />
 */
export function PromptList({ prompts, collections, loading, error, onRetry, onView, onEdit, onDelete, isFiltered }) {
  /**
   * Looks up the name of a collection by its ID.
   *
   * @param {string} id - The collection ID to search for.
   * @returns {string|undefined} The matching collection's name, or undefined if not found.
   *
   * @example
   * getCollectionName('abc123'); // 'Marketing Prompts'
   */
  const getCollectionName = (id) => collections.find((c) => c.id === id)?.name;

  if (loading) {
    return (
      <div className="flex justify-center items-center py-20" aria-label="Loading prompts">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={onRetry} />;
  }

  if (!prompts.length) {
    return isFiltered ? (
      <div className="flex flex-col items-center justify-center py-20 text-center">
        <div className="w-16 h-16 bg-gray-100 rounded-2xl flex items-center justify-center mb-4">
          <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <h3 className="text-gray-700 font-semibold mb-1">No results found</h3>
        <p className="text-sm text-gray-500">Try a different search term or collection.</p>
      </div>
    ) : (
      <div className="flex flex-col items-center justify-center py-20 text-center">
        <div className="w-16 h-16 bg-indigo-50 rounded-2xl flex items-center justify-center mb-4">
          <svg className="w-8 h-8 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h3 className="text-gray-700 font-semibold mb-1">No prompts yet</h3>
        <p className="text-sm text-gray-500">Click <strong>New Prompt</strong> to create your first one.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4" role="list" aria-label="Prompts">
      {prompts.map((prompt) => (
        <div key={prompt.id} role="listitem">
          <PromptCard
            prompt={prompt}
            collectionName={getCollectionName(prompt.collection_id)}
            onClick={() => onView(prompt)}
            onEdit={() => onEdit(prompt)}
            onDelete={() => onDelete(prompt)}
          />
        </div>
      ))}
    </div>
  );
}
