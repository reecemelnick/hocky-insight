export async function fetchScores(date) {
    const res = await fetch(`/api/scores?date=${date}`);
    if (!res.ok) {
        throw new Error("Failed to fetch scores");
    }
    return res.json();
}