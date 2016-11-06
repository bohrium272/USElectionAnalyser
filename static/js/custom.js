$(document).ready(function() {

    $.get('/locations', function(data){
        google.charts.load('upcoming', {'packages': ['geochart']});
        google.charts.setOnLoadCallback(function() {
            var map_data = [];
            map_data.push(['Country', 'Number of Tweets']);
            var keys = Object.keys(data);
            for(var i = 0 ; i < keys.length ; i++)
                if(keys[i] != 'NaN')
                    map_data.push([keys[i], data[keys[i]]]);
            var chart = new google.visualization.GeoChart(document.getElementById('tab_location'));
            chart.draw(google.visualization.arrayToDataTable(map_data), {});
        });    
    });

    $.get('/top_10_hashtags', function(data) {
        console.log('Loading Top 10');
        var chart_data = [];
        var keys = Object.keys(data)
        for(var i = 0 ; i < keys.length ; i++) 
            chart_data.push(data[keys[i]]);
        var ctx = document.getElementById('top10');
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: Object.keys(data),
                datasets: [{
                        label: 'Frequency',
                        data: chart_data,
                        borderWidth: 1,
                        backgroundColor: 'rgba(255, 206, 86, 1)'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero:true
                        }
                    }]
                }
            }
        });
    });

    $.get('/dist/original_fav', function(data) {
        var chart_data = [];
        console.log('Loading Top 10');
        var keys = Object.keys(data)
        for(var i = 0 ; i < keys.length ; i++) 
            chart_data.push(data[keys[i]]);
        var ctx = document.getElementById('orig_vs_fav');
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: Object.keys(data),
                datasets: [{
                        label: 'Number of Favorites',
                        data: chart_data,
                        borderWidth: 1,
                        backgroundColor: 'rgba(255, 206, 86, 1)'
                    }
                ]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero:true
                        }
                    }]
                }
            }
        });
    });

    $.get('/dist/original_retweet', function(data) {
        var chart_data = [];
        console.log('Loading Top 10');
        var keys = Object.keys(data)
        for(var i = 0 ; i < keys.length ; i++) 
            chart_data.push(data[keys[i]]);
        var ctx = document.getElementById('orig_vs_ret');
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: Object.keys(data),
                datasets: [{
                        label: 'Frequency',
                        data: chart_data,
                        borderWidth: 1,
                        backgroundColor: 'rgba(255, 206, 86, 1)'
                    }
                ]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero:true
                        }
                    }]
                }
            }
        });
    });

    $.get('/dist/mime_type', function(data) {
        var chart_data = [];
        console.log('Loading Top 10');
        var keys = Object.keys(data)
        for(var i = 0 ; i < keys.length ; i++) 
            chart_data.push(data[keys[i]]);
        var ctx = document.getElementById('mime_type');
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: Object.keys(data),
                datasets: [{
                        label: 'Frequency',
                        data: chart_data,
                        borderWidth: 1,
                        backgroundColor: 'rgba(255, 206, 86, 1)'
                    }
                ]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero:true
                        }
                    }]
                }
            }
        });
    });
});