import { useEffect, useRef } from "react";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);


export function useMedicationChart(medications) {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);


  function prepareMedicationData(medications) {
    const result = [];

    for (let i = 0; i < medications.length; i++) {
      const med = medications[i];

      result.push({
        label: med.name,
        stock: med.stock,
      });
    }

    return result;
  }


  function renderChart() {

    if (!chartRef.current) {
      return;
    }

    const context = chartRef.current.getContext("2d");

    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    const prepared = prepareMedicationData(medications);

    const labels = prepared.map(function (item) {
      return item.label;
    });

    const values = prepared.map(function (item) {
      return item.stock;
    });

    chartInstance.current = new Chart(context, {
      type: "bar",
      data: {
        labels,
        datasets: [{
          label: "Stock (mg)",
          data: values,
          backgroundColor: "#F34FBF",
          borderWidth: 0,
          borderRadius: 4,
          barPercentage: 0.8,
          categoryPercentage: 0.9,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              color: "#FFF",
              font: { size: 9 },
            },
            grid: {
              color: "#FFFFFF",
              drawBorder: true,
              borderColor: "#000",
              lineWidth: 0.5,
            }
          },

          x: {
            ticks: {
              color: "#FFF",
              font: { size: 9 },
            },
            grid: {
              color: "#FFFFFF",
              drawBorder: true,
              borderColor: "#000",
              lineWidth: 0.5,
            }
          }
        },

        plugins: {
          legend: { display: false },
        },

        layout: {
          padding: 10,
        }
      }
    });
  }


  useEffect(function () {
    renderChart();
  }, [medications]);


  return {
    chartRef
  };
}
