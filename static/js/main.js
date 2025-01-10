const ctx = document.getElementById('myChart');

new Chart(ctx,
    {
        type: 'line',

        data: {
          labels: dates,

          datasets: [
              {
                label: '# of Votes',
                data: valuesUSD,
                borderWidth: 1
              },
              {
                label: '# of Votes',
                data: valuesEUR,
                borderWidth: 1
              }
          ]
        },

        options: {
          scales: {
            y: {
              beginAtZero: false
            }
          }
        }

    }
);

console.log(dates)
console.log(values)
