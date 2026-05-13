export async function fetchPrediction(page = 1, season = "20262027", sort_by = "predicted_ppg", order = "DESC", position = "all") {
    const url = `/api/predict?page=${page}&season=${season}&sort=${sort_by}&order=${order}&position=${position}`
    const res = await fetch(url)
    if (!res.ok) {
        throw new Error("Failed to fetch predictions")
    }
    return res.json();
}