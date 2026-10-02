async function loadIncident() {

    const params =
        new URLSearchParams(
            window.location.search
        );

    const eventId =
        params.get("id");


    if (!eventId) {

        document.body.innerHTML =
            "<h2>Event ID not provided.</h2>";

        return;
    }


    try {

        const response =
            await fetch(
                `/alerts/${eventId}`
            );


        if (!response.ok) {

            throw new Error(
                "Security event not found."
            );
        }


        const event =
            await response.json();


        document.getElementById(
            "event-id"
        ).textContent =
            event.id;


        document.getElementById(
            "event-time"
        ).textContent =
            formatDate(
                event.created_at
            );


        document.getElementById(
            "classification"
        ).textContent =
            event.classification;


        document.getElementById(
            "attack-probability"
        ).textContent =
            `${(
                event.attack_probability * 100
            ).toFixed(2)}%`;


        document.getElementById(
            "risk-score"
        ).textContent =
            event.risk_score;


        document.getElementById(
            "risk-level"
        ).textContent =
            event.risk_level;


        document.getElementById(
            "anomaly"
        ).textContent =
            event.anomaly
                ? "YES"
                : "NO";


        document.getElementById(
            "anomaly-score"
        ).textContent =
            event.anomaly_score.toFixed(4);


        document.getElementById(
            "response"
        ).textContent =
            event.response_actions.join(
                ", "
            );


        await loadFeedback(eventId);


    } catch (error) {

        console.error(error);

    }
}


async function loadFeedback(eventId) {

    const container =
        document.getElementById(
            "feedback-container"
        );


    try {

        const response =
            await fetch(
                `/feedback/event/${eventId}`
            );


        if (!response.ok) {

            throw new Error(
                "Failed to load feedback."
            );
        }


        const feedback =
            await response.json();


        if (feedback.length === 0) {

            container.innerHTML =
                "<p>No analyst feedback yet.</p>";

            return;
        }


        container.innerHTML =
            feedback.map(
                item => `

                    <div class="feedback-box">

                        <span>
                            Analyst Classification
                        </span>

                        <strong>
                            ${item.analyst_label}
                        </strong>

                        <p style="margin-top:10px;">
                            ${item.analyst_comment || "No comment"}
                        </p>

                        <small>
                            ${formatDate(item.created_at)}
                        </small>

                    </div>

                `
            ).join("");


    } catch (error) {

        console.error(error);

        container.innerHTML =
            "<p>Unable to load feedback.</p>";

    }
}


async function submitFeedback() {

    const params =
        new URLSearchParams(
            window.location.search
        );

    const eventId =
        params.get("id");


    const analystLabel =
        document.getElementById(
            "analyst-label"
        ).value;


    const analystComment =
        document.getElementById(
            "analyst-comment"
        ).value.trim();


    const message =
        document.getElementById(
            "feedback-message"
        );


    try {

        const response =
            await fetch(
                "/feedback",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        event_id:
                            Number(eventId),

                        analyst_label:
                            analystLabel,

                        analyst_comment:
                            analystComment || null
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Failed to submit feedback."
            );
        }


        message.textContent =
            "Feedback submitted successfully.";


        message.style.color =
            "#22c55e";


        document.getElementById(
            "analyst-comment"
        ).value = "";


        await loadFeedback(eventId);


    } catch (error) {

        console.error(error);


        message.textContent =
            error.message;


        message.style.color =
            "#ef4444";

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
    loadIncident
);