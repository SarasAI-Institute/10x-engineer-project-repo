import { useState, useEffect } from "react";

function SearchBar({ onSearch }) {
  const [value, setValue] = useState("");

  useEffect(() => {
    const timeout = setTimeout(() => {
      onSearch(value);
    }, 500); // wait 500ms

    return () => clearTimeout(timeout);
  }, [value]);

  return (
    <input
      type="text"
      placeholder="Search prompts..."
      value={value}
      onChange={(e) => setValue(e.target.value)}
      className="w-full p-2 border rounded mb-4"
    />
  );
}

export default SearchBar;