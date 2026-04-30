const DEV_URL = process.env.REACT_APP_DEV_BACKEND || 'http://localhost:8000';

export async function fetchStandings() {
    let url = `${DEV_URL}/api/standings`
    const res = await fetch(url)
    if (!res.ok) {
        throw new Error("Failed to fetch standings")
    }
    return res.json();
}