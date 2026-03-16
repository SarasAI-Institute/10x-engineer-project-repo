import Header from './Header';
import Sidebar from './Sidebar';

function Layout({ children }) {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <Header />
      <div className="flex flex-col-reverse gap-4 px-4 pb-8 pt-4 lg:flex-row lg:pb-16 lg:pt-6">
        <Sidebar />
        <main className="flex-1 rounded-3xl border border-white/5 bg-slate-900/70 p-6 shadow-2xl shadow-slate-950/50 lg:p-10">
          {children}
        </main>
      </div>
    </div>
  );
}

export default Layout;
