function StandingsBoard( {standings} ) {

    return (
        <div style={{ marginBottom: "20px" }}>
            <table>
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Team</th>
                        <th>W</th>
                        <th>L</th>
                        <th>OTL</th>
                        <th>Points</th>
                    </tr>
                </thead>
                <tbody>
                    {standings.map((item, index) => (
                        <tr key={index}>
                            <td>{index + 1}</td>
                            <td>{item.team_name}</td>
                            <td>{item.wins}</td>
                            <td>{item.loss}</td>
                            <td>{item.otLoss}</td>
                            <td>{item.points}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}

export default StandingsBoard;