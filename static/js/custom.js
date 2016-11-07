$(document).ready(function() {
    
    /**
     * Function to Show the Loading Spinner
     */
    var showSpinner = function() {
        document.getElementById('spinner').style.display = 'block';
    }

    /**
     * Function to Hide the Loading Spinner
     */
    var hideSpinner =  function() {
        document.getElementById('spinner').style.display = 'none';
    }
    /**
     * Function to Show a Transient Snackbar Message
     */
    var showSnackBar = function() {
        var snackbarContainer = document.querySelector('#toast');
        snackbarContainer.MaterialSnackbar.showSnackbar({message: 'Failed to update due to a server error'});
    }

    //  Hide the Spinner
    hideSpinner();

    /**
     * Getting Location Data
     */
    $.get('/locations', function(data){
        console.log(data);
        google.charts.load('upcoming', {'packages': ['geochart']});
        google.charts.setOnLoadCallback(function() {
            var map_data = [];
            map_data.push(['Country', 'Number of Tweets']);
            var keys = Object.keys(data);
            for(var i = 0 ; i < keys.length ; i++)
                if(keys[i] != 'NaN' || keys[i] != 'null')
                    map_data.push([keys[i], data[keys[i]]]);
            var chart = new google.visualization.GeoChart(document.getElementById('tab_location'));
            chart.draw(google.visualization.arrayToDataTable(map_data), {});
        });    
    });

    /**
     * Getting Top 10 Hashtags
     */
    $.get('/top_10_hashtags', function(data) {
        var chart_data = [];
        var keys = Object.keys(data)
        for(var i = 0 ; i < keys.length ; i++) 
            chart_data.push(data[keys[i]]);
        var ctx = document.getElementById('top10').getContext('2d');
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


    /**
     * Getting Distibution of Favorites on Original Tweets
     */
    $.get('/dist/original_fav', function(data) {
        var chart_data = [];
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


    /**
     * Getting Distribution of Original Tweets vs Retweets
     */
    $.get('/dist/original_retweet', function(data) {
        var chart_data = [];
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

    /**
     * Geting Content Type of Tweets
     */
    $.get('/dist/mime_type', function(data) {
        var chart_data = [];
        var keys = Object.keys(data)
        for(var i = 0 ; i < keys.length ; i++) 
            chart_data.push(data[keys[i]]);
        var ctx = document.getElementById('mime_type');
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Text', 'Text + Image'],
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

    /**
     * Get number of Tweets Processed
     */
    $.get('/number_of_tweets', function(data) {
        var count = data['Count'];
        document.getElementById('count_label').innerHTML = count;
    });
    /**
     * Refreshing the Data
     */
    document.getElementById('refresh_button').onclick = function(event) {
        document.getElementById('refresh_button').disabled = 'disabled';
        showSpinner();
        $.get('/refresh_data', function(data) {
            if(data['Message'] === 'Failed!')
                showSnackBar();
            else {
                hideSpinner();
                location.reload();
                document.getElementById('refresh_button').disabled = '';    
            }
        });
    };
});