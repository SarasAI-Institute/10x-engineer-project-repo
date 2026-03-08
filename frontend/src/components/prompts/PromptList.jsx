import { PromptCard } from './PromptCard';
import { LoadingSpinner } from '../shared/LoadingSpinner';
import { ErrorMessage } from '../shared/ErrorMessage';

export function PromptList({ prompts, collections, loading, error, onRetry, onView, onEdit, onDelete, isFiltered }) {
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
