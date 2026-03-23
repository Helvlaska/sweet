import { useEffect, useRef } from "react";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);


export function useActivityChart(entries) {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);


  function aggregateDailyAverages(entries) {
    // group values by date
    const groupedByDate = {};

    entries.forEach(function(entry) {
      const date = entry.entry_date;
      const value = entry.duration;

      if (!groupedByDate[date]) {
        groupedByDate[date] = [];
      }

      groupedByDate[date].push(value);
    });

    // calculating the average for each date
    const averagesByDate = {};

    for (const date in groupedByDate) {
      const values = groupedByDate[date];
      let sum = 0;

      for (let i = 0; i < values.length; i++) {
        sum = sum + values[i];
      }

      const average = sum / values.length;

      averagesByDate[date] = average;
    }

    // generate last 7 days
    const today = new Date();
    const last7Days = [];

    for (let i = 6; i >= 0; i--) {
      const date = new Date(today);
      date.setDate(today.getDate() - i);

      const isoDate = date.toISOString().split("T")[0];

      last7Days.push(isoDate);
    }

    // construct chart data
    const result = [];

    for (let i = 0; i < last7Days.length; i++) {
      const date = last7Days[i];
      const label = new Date(date)
        .toLocaleDateString("fr-FR", { weekday: "long" })
        .charAt(0)
        .toUpperCase();
      const average = averagesByDate[date] || null;

      result.push({
        label: label,
        average: average
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

    const aggregated = aggregateDailyAverages(entries);
    const labels = aggregated.map(function (item) {
      return item.label;
    });

    const values = aggregated.map(function (item) {
      return item.average;
    });

    chartInstance.current = new Chart(context, {
      type: "bar",
      data: {
        labels,
        datasets: [{
          label: "Durée d’activité (minutes)",
          data: values,
          backgroundColor: "#D3BC00",
          borderWidth: 0,
          borderRadius: 4,
          barPercentage: 1,
          categoryPercentage: 0.9,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            grid: {display: false},
            ticks: {
              color: "#000",
              font: { size: 9 },
            }
          },
          y: {display: false},
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: function(context) {
                return context.raw + " min";
              }
            }
          }
        }
      },
      layout: {
        padding: 10
      }
    });
  }


  useEffect(function() {
    renderChart();
  }, [entries]);


  return {
    chartRef
  };
}

