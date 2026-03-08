/**
 * Controlled search input component with a leading search icon.
 *
 * Renders a text input preceded by an SVG magnifying-glass icon. The component
 * is fully controlled: the parent manages the current value and receives change
 * notifications via the `onChange` callback which receives the raw string value
 * (not a synthetic event).
 *
 * @param {Object} props - Component props.
 * @param {string} props.value - The current search input value (controlled).
 * @param {function(value: string): void} props.onChange - Called with the new string value on each keystroke.
 * @param {string} [props.placeholder='Search...'] - Placeholder text for the input.
 * @returns {JSX.Element} A relative-positioned wrapper containing an icon and text input.
 *
 * @example
 * const [query, setQuery] = useState('');
 *
 * <SearchBar
 *   value={query}
 *   onChange={setQuery}
 *   placeholder="Search prompts…"
 * />
 */
export function SearchBar({ value, onChange, placeholder = 'Search...' }) {
  return (
    <div className="relative">
      <svg
        className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400"
        fill="none" stroke="currentColor" viewBox="0 0 24 24"
      >
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full pl-9 pr-4 py-2 text-sm border border-gray-300 rounded-lg
          focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent
          bg-white placeholder-gray-400"
      />
    </div>
  );
}
