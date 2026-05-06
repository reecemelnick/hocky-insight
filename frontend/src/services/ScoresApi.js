export async function fetchScores(date) {
    let url = `http://localhost:8000/api/scores?date=${date}`
    const res = await fetch(url);
    if (!res.ok) {
        throw new Error("Failed to fetch scores");
    }
    return res.json();
}