function RankingBoard( {rankings} ) {

    return (
        <div style={{ marginBottom: "20px" }}>
            <table>
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Team</th>
                        <th>Elo</th>
                    </tr>
                </thead>
                <tbody>
                    {rankings.map((item, index) => (
                        <tr key={index}>
                            <td>{index + 1}</td>
                            <td>{item.team_name}</td>
                            <td>{item.elo}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}

export default RankingBoard;