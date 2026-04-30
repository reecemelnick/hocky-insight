import { Link, useLocation } from "react-router-dom";

function NavigationBar() {
    const location = useLocation();

    const isActive = (path) => location.pathname === path;

    const navItems = [
        { path: "/", label: "Home" },
        { path: "/scores", label: "Scores" },
        { path: "/predict", label: "Predict" },
        { path: "/rankings", label: "Rankings" },
    ];

    return (
        <nav className="border-b border-slate-800 bg-slate-950 shadow-lg shadow-sky-950/20">
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                <div className="flex h-16 items-center justify-between">
                    <Link to="/" className="flex items-center gap-2">
                        <div className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-sky-400 bg-clip-text text-transparent">
                            Hockey Insight
                        </div>
                    </Link>

                    <div className="flex gap-1">
                        {navItems.map((item) => (
                            <Link
                                key={item.path}
                                to={item.path}
                                className={`px-4 py-2 text-sm font-semibold transition-colors duration-150 ${
                                    isActive(item.path)
                                        ? "border-b-2 border-cyan-400 text-cyan-400"
                                        : "text-slate-400 hover:text-white"
                                }`}
                            >
                                {item.label}
                            </Link>
                        ))}
                    </div>
                </div>
            </div>
        </nav>
    );
}

export default NavigationBar;
