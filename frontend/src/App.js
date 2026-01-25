import { BrowserRouter, Routes, Route } from "react-router-dom";
import ScoresPage from "./pages/ScoresPage";
import LandingPage from "./pages/LandingPage";
import GamePredictorPage from "./pages/GamePredictorPage";
import RankingPage from "./pages/RankingPage";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/scores" element={<ScoresPage />} />
                <Route path="/predict" element={<GamePredictorPage />} />
                <Route path="/rankings" element={<RankingPage />} />
            </Routes>
        </BrowserRouter>
    )
}
export default App;

// If it fetches data → page

// If it’s reused → component

// If it talks to backend → service

// If it wires routes → App