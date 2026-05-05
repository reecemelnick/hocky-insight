import { BrowserRouter, Routes, Route } from "react-router-dom";
import ScoresPage from "./pages/ScoresPage";
import LandingPage from "./pages/LandingPage";
import GamePredictorPage from "./pages/GamePredictorPage";
import RankingPage from "./pages/RankingPage";
import NavigationBar from "./components/NavigationBar";

function App() {
    return (
        <BrowserRouter>
            <NavigationBar />
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
