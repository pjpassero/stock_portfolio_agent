import {
    Chart as ChartJS,
    ArcElement,
    Tooltip
} from "chart.js";

import { Doughnut } from "react-chartjs-2";

ChartJS.register(ArcElement, Tooltip);

interface PortfolioScoreDialProps {
    score: number;
}

function getScoreColor(score: number): string {
    const clamped = Math.max(0, Math.min(100, score));

    if (clamped < 60) {
        // Dark red -> lighter red as score approaches 60
        const lightness = 30 + (clamped / 60) * 20;

        return `hsl(0, 75%, ${lightness}%)`;
    }

    // 60 -> 100 gradually becomes a stronger green
    const progress = (clamped - 60) / 40;

    const hue = 90 + progress * 30;
    const lightness = 50 - progress * 15;

    return `hsl(${hue}, 65%, ${lightness}%)`;
}

export default function PortfolioScoreDial({
    score
}: PortfolioScoreDialProps) {

    const normalizedScore = Math.max(
        0,
        Math.min(100, Number(score))
    );

    const scoreColor = getScoreColor(normalizedScore);

    const data = {
        datasets: [
            {
                data: [
                    normalizedScore,
                    100 - normalizedScore
                ],
                backgroundColor: [
                    scoreColor,
                    "#e9ecef"
                ],
                borderWidth: 0,
                circumference: 180,
                rotation: 270
            }
        ]
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        cutout: "75%",
        plugins: {
            tooltip: {
                enabled: false
            }
        }
    };

    return (
        <div
            style={{
                width: "500px",
                height: "200px",
                position: "relative"
            }}
        >
            <Doughnut
                data={data}
                options={options}
            />

            <div
                style={{
                    position: "absolute",
                    left: "50%",
                    bottom: "15px",
                    transform: "translateX(-50%)",
                    textAlign: "center"
                }}
            >
                <div
                    style={{
                        fontSize: "36px",
                        fontWeight: "bold",
                        color: scoreColor
                    }}
                >
                    {normalizedScore.toFixed(0)}
                </div>

                <div
                    style={{
                        fontSize: "14px"
                    }}
                >
                    Portfolio Score
                </div>
            </div>
        </div>
    );
}