async function loadDashboard() {

    try {

        const response = await fetch(
            "/alerts?limit=100"
        );

        if (!response.ok) {
            throw new Error(
                "Failed to load alerts"
            );
        }

        const events = await response.json();

        updateSummary(events);
        updateEventsTable(events);

        await loadFeedbackStats();

    } catch (error) {

        console.error(
            "Dashboard error:",
            error
        );

        document.getElementById(
            "events-table"
        ).innerHTML = `
            <tr>
                <td colspan="8">
                    Failed to load security events.
                </td>
            </tr>
        `;
    }
}


function updateSummary(events) {

    const high = events.filter(
        event => event.risk_level === "HIGH"
    ).length;

    const medium = events.filter(
        event => event.risk_level === "MEDIUM"
    ).length;

    const low = events.filter(
        event => event.risk_level === "LOW"
    ).length;


    document.getElementById(
        "total-events"
    ).textContent = events.length;


    document.getElementById(
        "high-risk"
    ).textContent = high;


    document.getElementById(
        "medium-risk"
    ).textContent = medium;


    document.getElementById(
        "low-risk"
    ).textContent = low;
}


function updateEventsTable(events) {

    const table = document.getElementById(
        "events-table"
    );


    if (events.length === 0) {

        table.innerHTML = `
            <tr>
                <td colspan="8">
                    No security events found.
                </td>
            </tr>
        `;

        return;
    }


    table.innerHTML = events.map(
        event => {

            const riskClass =
                event.risk_level === "HIGH"
                    ? "badge-high"
                    : event.risk_level === "MEDIUM"
                        ? "badge-medium"
                        : "badge-low";


            const probability =
                (
                    event.attack_probability * 100
                ).toFixed(2);


            const anomaly =
                event.anomaly
                    ? "YES"
                    : "NO";


            const response =
                event.response_actions
                    .join(", ");


            return `
                <tr>

                    <td>
                        <a
                            href="/dashboard/incident?id=${event.id}"
                            style="
                                color: #60a5fa;
                                font-weight: bold;
                                text-decoration: none;
                            "
                        >
                            #${event.id}
                        </a>
                    </td>

                    <td>
                        ${formatDate(event.created_at)}
                    </td>

                    <td>
                        ${event.classification}
                    </td>

                    <td>
                        ${probability}%
                    </td>

                    <td>
                        ${anomaly}
                    </td>

                    <td>
                        ${event.risk_score}
                    </td>

                    <td>
                        <span
                            class="badge ${riskClass}"
                        >
                            ${event.risk_level}
                        </span>
                    </td>

                    <td>
                        ${response}
                    </td>

                </tr>
            `;
        }
    ).join("");
}


async function loadFeedbackStats() {

    try {

        const response = await fetch(
            "/feedback/stats"
        );

        if (!response.ok) {
            throw new Error(
                "Failed to load feedback statistics"
            );
        }

        const stats = await response.json();


        document.getElementById(
            "total-feedback"
        ).textContent =
            stats.total_feedback;


        document.getElementById(
            "benign-feedback"
        ).textContent =
            stats.benign_feedback;


        document.getElementById(
            "attack-feedback"
        ).textContent =
            stats.attack_feedback;


        document.getElementById(
            "adaptation-status"
        ).textContent =
            stats.adaptation_status;

    } catch (error) {

        console.error(
            "Feedback statistics error:",
            error
        );

    }
}


function formatDate(value) {

    if (!value) {
        return "-";
    }

    return new Date(value)
        .toLocaleString();
}


document.addEventListener(
    "DOMContentLoaded",
    () => {

        loadDashboard();

        setInterval(
            loadDashboard,
            30000
        );

    }
);