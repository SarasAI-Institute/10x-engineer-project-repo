function CollectionList({ collections, selected, onSelect }) {
  return (
    <div className="mb-6">
      <h2 className="font-semibold mb-2">Collections</h2>

      <div className="flex gap-2 flex-wrap">
        <button
          onClick={() => onSelect(null)}
          className={`px-3 py-1 rounded ${
            selected === null ? "bg-black text-white" : "bg-gray-200"
          }`}
        >
          All
        </button>

        {collections.map((c) => (
          <button
            key={c.id}
            onClick={() => onSelect(c.id)}
            className={`px-3 py-1 rounded ${
              selected === c.id ? "bg-black text-white" : "bg-gray-200"
            }`}
          >
            {c.name}
          </button>
        ))}
      </div>
    </div>
  );
}

export default CollectionList;