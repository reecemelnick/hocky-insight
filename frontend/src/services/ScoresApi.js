export async function fetchScores(date) {
    const res = await fetch(`http://127.0.0.1:8000/scores?date=${date}`);
    if (!res.ok) {
        throw new Error("Failed to fetch scores");
    }
    return res.json();
}