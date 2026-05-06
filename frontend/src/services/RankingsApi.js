export async function fetchRankings() {
    let url = `http://localhost:8000/api/rankings`
    const res = await fetch(url)
    if (!res.ok) {
        throw new Error("Failed to fetch rankings")
    }
    return res.json();
}