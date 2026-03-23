import { useEffect, useRef } from "react";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);


export function useGlycemiaChart(entries) {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);


  function aggregateDailyAverages(entries) {
    // group values by date
    const groupedByDate = {};

    entries.forEach(function(entry) {
      const date = entry.entry_date;
      const value = entry.glucose_level;

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
      type: "line",
      data: {
        labels: labels,
        datasets: [{
          label: "Taux de glycémie (mg/l)",
          data: values,
          borderColor: "#FFFFFF",
          backgroundColor: "rgba(255,255,255,1)",
          borderWidth: 1,
          tension: 0,
          pointRadius: 6,
          pointBackgroundColor: "#FFFFFF",
          pointHoverRadius: 10,
          pointBorderColor:"#FFFFFF",
          fill: false
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            min: 50,
            max: 300,
            ticks: {
              stepSize: 50,
              callback: function (value) {
                return value + "mg";
              }
            }
          }
        },
        plugins: {
          legend: { display: false }
        }
      }
    });
  }


  useEffect(function () {
    renderChart();
  }, [entries]);


  return {
    chartRef
  };
}
