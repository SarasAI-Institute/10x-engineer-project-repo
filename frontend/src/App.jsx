import React from 'react'
import PromptList from './components/PromptList'
import Collections from './components/Collections'

export default function App() {
  return (
    <div className="app">
      <header className="header" role="banner">
        <div className="header-inner">
          <h1>PromptLab</h1>
          <p className="subtitle">Create and manage prompts</p>
        </div>
      </header>

      <main className="main">
        <aside className="sidebar">
          <Collections />
        </aside>
        <section className="content">
          <PromptList />
        </section>
      </main>

      <footer className="footer">PromptLab — Frontend (development)</footer>
    </div>
  )
}
