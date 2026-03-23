import { useEffect, useRef } from "react";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);


export function useWeightChart(entries, rangeType) {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);


  function aggregateWeightData(entries, rangeType) {
    const groupedByDate = {};

    entries.forEach(function(entry) {
      const date = entry.entry_date;
      const value = entry.mass;

      if (!groupedByDate[date]) {
        groupedByDate[date] = [];
      }

      groupedByDate[date].push(value);
    });


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


    const today = new Date();
    let startDate = null;

    if (rangeType === "week") {
      startDate = new Date(today);
      startDate.setDate(today.getDate() - 6);
    }

    if (rangeType === "month") {
      startDate = new Date(today);
      startDate.setDate(today.getDate() - 29);
    }

    if (rangeType === "3months") {
      startDate = new Date(today);
      startDate.setMonth(today.getMonth() - 2);
    }

    if (rangeType === "6months") {
      startDate = new Date(today);
      startDate.setMonth(today.getMonth() - 5);
    }


    const completeRange = [];
    const currentDate = new Date(startDate);

    while (currentDate <= today) {
      const formattedDate = new Date(currentDate);
      const isoDate = formattedDate.toISOString().split("T")[0];
      let average = null;

      if (averagesByDate[isoDate] !== undefined) {
        average = averagesByDate[isoDate];
      }

      completeRange.push({
        date: formattedDate,
        average: average
      });

      currentDate.setDate(currentDate.getDate() + 1);
    }

    return completeRange;
  }


  function renderChart() {

    if (!chartRef.current) {
      return;
    }

    const context = chartRef.current.getContext("2d");

    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    const aggregated = aggregateWeightData(entries, rangeType);
    const labels = aggregated.map(function(item) {
      return item.date.toLocaleDateString("fr-FR", {
        day: "2-digit",
        month: "short"
      });
    });

    const values = aggregated.map(function(item) {
      return item.average;
    });


    const validValues = values.filter(function(value) {
      return typeof value === "number";
    });


    let avg = 70;

    if (validValues.length > 0) {
      let sum = 0;

      for (let i = 0; i < validValues.length; i++) {
        sum = sum + validValues[i];
      }

      avg = sum / validValues.length;
    }


    const yMin = Math.floor((avg - 10) / 5) * 5;
    const yMax = Math.ceil((avg + 10) / 5) * 5;


    chartInstance.current = new Chart(context, {
      type: "line",
      data: {
        labels: labels,
        datasets: [{
          label: "Poids (kg)",
          data: values,
          spanGaps: false,
          borderColor: "#72655A",
          backgroundColor: "#FFFFFF",
          borderWidth: 1,
          fill: false,
          tension: 0,
          pointRadius: 6,
          pointBackgroundColor: "#FFFFFF",
          pointBorderWidth: 0,
          pointHoverRadius: 10,
          pointHoverBackgroundColor: "#FFFFFF",
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            min: yMin,
            max: yMax,
            ticks: {
              stepSize: 5,
              callback: function(value) {
                return value + "kg";
              },
              color: "#FFF",
              font: { size: 9 }
            },
            grid: {
              color: "#FFFFFF",
              drawBorder: true,
              borderColor: "#000",
              lineWidth: 1
            }
          },
          x: {
            ticks: {
              color: "#FFF",
              font: { size: 9 }
            },
            grid: {
              color: "#FFFFFF",
              drawBorder: true,
              borderColor: "#000",
              lineWidth: 1
            }
          }
        },
        plugins: {
          legend: { display: false }
        },
        layout: {
          padding: 10
        }
      }
    });
  }


  useEffect(function () {
    renderChart();
  }, [entries, rangeType]);


  return {
    chartRef
  };
}
