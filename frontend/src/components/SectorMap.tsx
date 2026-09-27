import { Pie } from "react-chartjs-2"

import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend
} from "chart.js"

ChartJS.register(ArcElement, Tooltip, Legend)


interface Position {
    ticker: string;
    sector: string | null;
    allocation: number;
    assetClass: string;
}

interface Props {
    portfolioExpanded: Position[];
}

export default function SectorPieChart({ portfolioExpanded }: Props) {
    const sector_weights: Record<string, number> = {};

    portfolioExpanded.forEach((position) => {
        const sector =
            position.sector === null ||
                position.assetClass === "CASH" ||
                position.assetClass === "ETF"
                ? "Other"
                : position.sector;

        sector_weights[sector] =
            (sector_weights[sector] || 0) + position.allocation;
    });

    const chart_data = {
        labels: Object.keys(sector_weights),
        datasets: [
            {
                label: "Allocation",
                data: Object.values(sector_weights).map(
                    weight => weight * 100
                ),
                backgroundColor: [
                    "#0d6efd",
                    "#6f42c1",
                    "#198754",
                    "#ffc107",
                    "#dc3545"
                ]
            }
        ]
    };
    return (
        <Pie
            data={chart_data}
            options={{
                responsive: true,

                plugins: {
                    legend: {
                        position: "bottom"
                    },

                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                const value = context.raw as number;

                                return `${context.label}: ${value.toFixed(2)}%`;
                            }
                        }
                    }
                }
            }}
        />
    )

}
