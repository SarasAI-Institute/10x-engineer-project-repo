/**
 * Card component displaying a summary of a single prompt.
 *
 * Renders a clickable card showing the prompt title, optional description,
 * a monospace preview of the content, the collection badge, and the last
 * updated date. Edit and delete icon buttons are overlaid in the top-right
 * corner; their click events are stopped from bubbling to the card's
 * `onClick` handler.
 *
 * @param {Object} props - Component props.
 * @param {{
 *   id: string,
 *   title: string,
 *   content: string,
 *   description?: string,
 *   collection_id?: string,
 *   updated_at: string
 * }} props.prompt - The prompt data to display.
 * @param {string} [props.collectionName] - Human-readable name of the prompt's collection.
 *   When falsy no collection badge is rendered.
 * @param {function(): void} props.onClick - Called when the user clicks the card body (opens detail view).
 * @param {function(): void} props.onEdit - Called when the user clicks the edit icon button.
 * @param {function(): void} props.onDelete - Called when the user clicks the delete icon button.
 * @returns {JSX.Element} A styled card element summarising the prompt.
 *
 * @example
 * <PromptCard
 *   prompt={prompt}
 *   collectionName="Marketing"
 *   onClick={() => setViewingPrompt(prompt)}
 *   onEdit={() => openEdit(prompt)}
 *   onDelete={() => handleDeletePrompt(prompt)}
 * />
 */
export function PromptCard({ prompt, collectionName, onClick, onEdit, onDelete }) {
  /**
   * Formats an ISO date string into a short human-readable date.
   *
   * @param {string} iso - An ISO 8601 date string (e.g. '2024-03-08T12:00:00Z').
   * @returns {string} Formatted date such as 'Mar 8, 2024'.
   *
   * @example
   * formatDate('2024-03-08T12:00:00Z'); // 'Mar 8, 2024'
   */
  const formatDate = (iso) => new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });

  return (
    <div
      onClick={onClick}
      className="bg-white rounded-xl border border-gray-200 p-5 hover:border-indigo-300 hover:shadow-md
        transition-all cursor-pointer group"
    >
      <div className="flex items-start justify-between gap-3 mb-3">
        <h3 className="font-semibold text-gray-900 text-sm leading-snug line-clamp-2 group-hover:text-indigo-700 transition-colors">
          {prompt.title}
        </h3>
        <div className="flex gap-1 shrink-0" onClick={(e) => e.stopPropagation()}>
          <button
            onClick={onEdit}
            className="p-1.5 text-gray-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors cursor-pointer"
            title="Edit"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </button>
          <button
            onClick={onDelete}
            className="p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors cursor-pointer"
            title="Delete"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>

      {prompt.description && (
        <p className="text-xs text-gray-500 mb-3 line-clamp-2">{prompt.description}</p>
      )}

      <p className="text-xs text-gray-600 bg-gray-50 rounded-lg p-2.5 line-clamp-3 font-mono leading-relaxed mb-3">
        {prompt.content}
      </p>

      <div className="flex items-center justify-between">
        {collectionName ? (
          <span className="text-xs bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded-full font-medium">
            {collectionName}
          </span>
        ) : (
          <span />
        )}
        <span className="text-xs text-gray-400">{formatDate(prompt.updated_at)}</span>
      </div>
    </div>
  );
}
