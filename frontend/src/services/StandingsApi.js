export async function fetchStandings() {
    let url = `http://localhost:8000/api/standings`
    const res = await fetch(url)
    if (!res.ok) {
        throw new Error("Failed to fetch standings")
    }
    return res.json();
}