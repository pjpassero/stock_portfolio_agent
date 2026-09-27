import { Pie } from "react-chartjs-2";

import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend
} from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

interface Position {
    ticker: string;
    allocation: number;
}

interface Props {
    portfolioExpanded: Position[];
}

export default function TickerPieChart({ portfolioExpanded }: Props) {

    const chart_data = {
        labels: portfolioExpanded.map(
            position => position.ticker
        ),

        datasets: [
            {
                label: "Allocation",

                data: portfolioExpanded.map(
                    position => position.allocation * 100
                ),

                backgroundColor: [
                    "#0d6efd",
                    "#6f42c1",
                    "#198754",
                    "#ffc107",
                    "#dc3545",
                    "#0dcaf0",
                    "#fd7e14",
                    "#20c997",
                    "#6610f2",
                    "#d63384",
                    "#6c757d"
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
    );
}