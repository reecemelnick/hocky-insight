export async function fetchScores(date) {
    const res = await fetch(`http://165.232.57.251:8000/scores?date=${date}`);
    if (!res.ok) {
        throw new Error("Failed to fetch scores");
    }
    return res.json();
}