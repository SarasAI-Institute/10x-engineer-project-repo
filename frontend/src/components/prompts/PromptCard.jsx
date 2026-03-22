function PromptCard({ prompt, onDelete, onEdit }) {
  return (
    <div className="bg-white p-4 rounded-xl shadow hover:shadow-lg transition">
      <h3 className="text-lg font-semibold">{prompt.title}</h3>

      <p className="text-gray-600 mt-2 line-clamp-3">
        {prompt.content}
      </p>

      <div className="mt-4 flex justify-between items-center">
        <button
          onClick={() => onEdit(prompt)}
          className="text-blue-600 text-sm hover:underline"
        >
          Edit
        </button>

        <button
          onClick={() => {
            if (confirm("Are you sure you want to delete this prompt?")) {
              onDelete(prompt.id);
            }
          }}
          className="text-red-600 text-sm hover:underline"
        >
          Delete
        </button>
      </div>
    </div>
  );
}

export default PromptCard;