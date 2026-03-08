import { LoadingSpinner } from '../shared/LoadingSpinner';
import { ErrorMessage } from '../shared/ErrorMessage';

/**
 * Renders the list of collections in the sidebar navigation.
 *
 * Handles three loading/data states before rendering the list:
 * 1. **Loading** — shows a centred `LoadingSpinner`.
 * 2. **Error** — shows an `ErrorMessage`.
 * 3. **Empty** — shows a "No collections yet." placeholder message.
 *
 * Each collection row contains a selection button and an optional delete
 * button that appears on hover via CSS group-hover.
 *
 * @param {Object} props - Component props.
 * @param {Array<{id: string, name: string, description?: string}>} props.collections - Collections to display.
 * @param {boolean} [props.loading] - When true, renders a loading spinner instead of the list.
 * @param {string} [props.error] - Error message string; when truthy renders an `ErrorMessage`.
 * @param {string|null} props.selectedId - ID of the currently selected collection; highlighted if matched.
 * @param {function(id: string): void} props.onSelect - Called when the user clicks a collection row.
 * @param {function(id: string): void} [props.onDelete] - Called when the user clicks the delete icon.
 *   When omitted the delete button is not rendered.
 * @returns {JSX.Element} A loading spinner, error message, empty state, or a `<ul>` of collection rows.
 *
 * @example
 * <CollectionList
 *   collections={collections}
 *   selectedId={selectedCollection}
 *   onSelect={setSelectedCollection}
 *   onDelete={handleDeleteCollection}
 * />
 */
export function CollectionList({ collections, loading, error, selectedId, onSelect, onDelete }) {
  if (loading) {
    return (
      <div className="flex justify-center py-8">
        <LoadingSpinner />
      </div>
    );
  }

  if (error) {
    return <ErrorMessage message={error} />;
  }

  if (!collections.length) {
    return (
      <p className="text-sm text-gray-400 px-3 py-4 text-center">No collections yet.</p>
    );
  }

  return (
    <ul className="space-y-1">
      {collections.map((col) => (
        <li key={col.id} className="flex items-center group">
          <button
            onClick={() => onSelect(col.id)}
            className={`flex-1 text-left px-3 py-2 rounded-lg text-sm transition-colors cursor-pointer
              ${selectedId === col.id
                ? 'bg-indigo-50 text-indigo-700 font-medium'
                : 'text-gray-700 hover:bg-gray-100'}`}
          >
            <span className="block truncate">{col.name}</span>
            {col.description && (
              <span className="block text-xs text-gray-400 truncate mt-0.5">{col.description}</span>
            )}
          </button>
          {onDelete && (
            <button
              onClick={() => onDelete(col.id)}
              className="opacity-0 group-hover:opacity-100 p-1 mr-1 text-gray-400
                hover:text-red-500 transition-all cursor-pointer"
              title="Delete collection"
            >
              <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          )}
        </li>
      ))}
    </ul>
  );
}
