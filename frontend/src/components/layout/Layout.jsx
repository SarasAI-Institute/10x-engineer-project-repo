import { useState } from 'react';
import { Header } from './Header';
import { Sidebar } from './Sidebar';

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
