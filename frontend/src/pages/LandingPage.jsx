import { Link } from "react-router-dom";

function LandingPage() {
    const features = [
        {
            title: "Game Scores",
            description: "View NHL game scores and results for any date. See team ELO ratings and match outcomes with an intuitive date selector.",
            link: "/scores",
            icon: "🏒",
        },
        {
            title: "Player Predictions",
            description: "Analyze player performance predictions for the 2024-2025 season. Compare predicted points per game with actual performance data.",
            link: "/predict",
            icon: "📊",
        },
        {
            title: "Team Rankings",
            description: "Explore team power rankings based on ELO ratings and compare them with official NHL standings. See how teams rank against each other.",
            link: "/rankings",
            icon: "🏆",
        },
    ];

    return (
        <div className="min-h-screen bg-slate-950 px-4 py-10 text-slate-100 sm:px-6 lg:px-8">
            <div className="mx-auto max-w-6xl space-y-12">
                {/* Hero Section */}
                <div className="space-y-6 text-center">
                    <div className="space-y-2">
                        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-cyan-400">Welcome to</p>
                        <h1 className="text-5xl font-bold tracking-tight text-white sm:text-6xl">
                            Hockey Insight
                        </h1>
                    </div>
                    <p className="mx-auto max-w-2xl text-lg leading-8 text-slate-300">
                        Advanced NHL analytics powered by ELO ratings, predictive modeling, and real-time game data. Make informed decisions with data-driven insights.
                    </p>
                    <div className="flex justify-center gap-4 pt-4">
                        <Link
                            to="/scores"
                            className="rounded-lg border border-cyan-500 bg-cyan-500/10 px-6 py-3 font-semibold text-cyan-400 hover:bg-cyan-500/20 transition-colors"
                        >
                            Get Started
                        </Link>
                        <Link
                            to="/rankings"
                            className="rounded-lg border border-slate-700 px-6 py-3 font-semibold text-slate-300 hover:bg-slate-800 transition-colors"
                        >
                            View Rankings
                        </Link>
                    </div>
                </div>

                {/* Features Grid */}
                <div className="grid gap-6 md:grid-cols-3">
                    {features.map((feature) => (
                        <Link
                            key={feature.link}
                            to={feature.link}
                            className="group rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-2xl shadow-sky-950/20 backdrop-blur transition-all duration-150 hover:border-slate-700 hover:bg-slate-800/80"
                        >
                            <div className="space-y-4">
                                <div className="text-4xl">{feature.icon}</div>
                                <h3 className="text-xl font-bold text-white group-hover:text-cyan-400 transition-colors">
                                    {feature.title}
                                </h3>
                                <p className="text-sm leading-6 text-slate-400">
                                    {feature.description}
                                </p>
                                <div className="text-xs font-semibold uppercase tracking-[0.2em] text-cyan-400/60 group-hover:text-cyan-400 transition-colors">
                                    Explore →
                                </div>
                            </div>
                        </Link>
                    ))}
                </div>

                {/* Info Section */}
                <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-8 shadow-2xl shadow-sky-950/30 backdrop-blur">
                    <h2 className="text-2xl font-bold text-white mb-4">About Hockey Insight</h2>
                    <div className="space-y-3 text-slate-300">
                        <p>
                            Hockey Insight combines historical NHL data with advanced ELO rating algorithms to provide predictive analytics for games and player performance.
                        </p>
                        <p>
                            Our platform leverages machine learning models trained on multiple seasons of NHL history to forecast player point production and team strength.
                        </p>
                        <p>
                            Whether you're a casual fan or serious analyst, use our tools to understand team dynamics, predict future performance, and explore the data behind the game.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default LandingPage;