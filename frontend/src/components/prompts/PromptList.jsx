import PromptCard from "./PromptCard";

function PromptList({ prompts, onDelete, onEdit }) {
  if (prompts.length === 0) {
    return (
      <div className="text-center text-gray-400 py-10">
        No prompts found 🚀
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {prompts.map((p) => (
        <PromptCard
          key={p.id}
          prompt={p}
          onDelete={onDelete}
          onEdit={onEdit}
        />
      ))}
    </div>
  );
}

export default PromptList;