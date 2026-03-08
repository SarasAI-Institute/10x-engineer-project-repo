import { useState } from 'react';
import { Header } from './Header';
import { Sidebar } from './Sidebar';

/**
 * Root application layout component providing a responsive shell with header,
 * collapsible sidebar, and main content area.
 *
 * On mobile the sidebar is hidden by default and slides in as a drawer when
 * the hamburger button in the `Header` is clicked. A semi-transparent overlay
 * is rendered behind the open drawer; clicking it closes the sidebar. On
 * large screens (`lg:`) the sidebar is always visible alongside the main
 * content area.
 *
 * @param {Object} props - Component props.
 * @param {Array<Object>} props.collections - List of collection objects to pass to the Sidebar.
 * @param {string|null} props.selectedCollection - ID of the currently selected collection, or null.
 * @param {function(id: string|null): void} props.onSelectCollection - Called when a collection
 *   is selected in the sidebar. Also closes the mobile drawer.
 * @param {function(collection: Object): void} props.onCollectionCreated - Called after a new
 *   collection is successfully created.
 * @param {function(id: string): void} props.onDeleteCollection - Called when a collection
 *   delete is requested from the sidebar.
 * @param {React.ReactNode} props.children - Page content rendered inside the `<main>` element.
 * @returns {JSX.Element} Full-height flex layout with header, sidebar, and main.
 *
 * @example
 * <Layout
 *   collections={collections}
 *   selectedCollection={selectedCollection}
 *   onSelectCollection={setSelectedCollection}
 *   onCollectionCreated={fetchCollections}
 *   onDeleteCollection={handleDeleteCollection}
 * >
 *   <PromptList ... />
 * </Layout>
 */
export function Layout({ collections, selectedCollection, onSelectCollection, onCollectionCreated, onDeleteCollection, children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex flex-col h-screen">
      <Header onMenuClick={() => setSidebarOpen(true)} />
      <div className="flex flex-1 overflow-hidden">
        {/* Mobile overlay */}
        {sidebarOpen && (
          <div
            className="fixed inset-0 z-30 bg-black/40 lg:hidden"
            onClick={() => setSidebarOpen(false)}
            aria-hidden="true"
          />
        )}

        {/* Sidebar — hidden on mobile unless open */}
        <div className={`
          fixed inset-y-0 left-0 z-40 w-64 transform transition-transform duration-200
          lg:relative lg:translate-x-0 lg:z-auto
          ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
        `}>
          <Sidebar
            collections={collections}
            selectedCollection={selectedCollection}
            onSelectCollection={(id) => { onSelectCollection(id); setSidebarOpen(false); }}
            onCollectionCreated={onCollectionCreated}
            onDeleteCollection={onDeleteCollection}
          />
        </div>

        <main className="flex-1 overflow-y-auto bg-gray-50 min-w-0">
          {children}
        </main>
      </div>
    </div>
  );
}
