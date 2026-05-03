const DEV_URL = process.env.REACT_APP_DEV_BACKEND || 'http://localhost:8000';

export async function fetchScores(date) {
    let url = `${DEV_URL}/api/scores?date=${date}`
    const res = await fetch(url);
    if (!res.ok) {
        throw new Error("Failed to fetch scores");
    }
    return res.json();
}