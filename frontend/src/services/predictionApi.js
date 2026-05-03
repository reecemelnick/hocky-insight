export async function fetchPrediction() {
    const baseUrl = process.env.REACT_APP_DEV_BACKEND || 'http://localhost:8000'
    const url = `${baseUrl}/api/predict`
    const res = await fetch(url)
    if (!res.ok) {
        throw new Error("Failed to fetch predictions")
    }
    return res.json();
}