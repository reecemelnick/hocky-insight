const DEV_URL = process.env.REACT_APP_DEV_BACKEND;

export async function fetchStandings() {
    let url = '/api/standings'
    const res = await fetch(url)
    if (!res.ok) {
        throw new Error("Failed to fetch standings")
    }
    return res.json();
}