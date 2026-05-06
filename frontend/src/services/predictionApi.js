export async function fetchPrediction(page = 1) {
    const url = `http://localhost:8000/api/predict?page=${page}`
    const res = await fetch(url)
    if (!res.ok) {
        throw new Error("Failed to fetch predictions")
    }
    return res.json();
}