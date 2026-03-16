import PromptCard from './PromptCard';
import EmptyState from '../shared/EmptyState';

function PromptList({ prompts, onSelect, selectedId, collectionLookup = {}, emptyActionProps }) {
  if (!prompts.length) {
    return (
      <EmptyState
        title="No prompts found"
        description="Try creating a prompt to get started or adjust your search query."
        actionText="Create prompt"
        actionProps={{ type: 'button', ...emptyActionProps }}
      />
    );
  }

  return (
    <div className="grid gap-4 md:grid-cols-2">
      {prompts.map((prompt) => (
        <PromptCard
          key={prompt.id}
          prompt={prompt}
          onSelect={onSelect}
          isSelected={prompt.id === selectedId}
          collectionName={collectionLookup[prompt.collection_id]}
        />
      ))}
    </div>
  );
}

export default PromptList;
