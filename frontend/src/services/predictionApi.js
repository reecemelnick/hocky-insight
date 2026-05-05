export async function fetchPrediction() {
    const url = `/api/predict`
    const res = await fetch(url)
    if (!res.ok) {
        throw new Error("Failed to fetch predictions")
    }
    return res.json();
}