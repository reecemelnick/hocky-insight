export async function fetchScores(date) {
    let url = `/api/scores?date=${date}`
    const res = await fetch(url);
    if (!res.ok) {
        throw new Error("Failed to fetch scores");
    }
    return res.json();
}