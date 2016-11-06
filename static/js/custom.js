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
        google.charts.load('current', {packages: ['corechart']});
        google.charts.setOnLoadCallback(function() {
            var chart_data = [];
            var keys = Object.keys(data)
            chart_data.push(['Hashtag', 'Frequency']);
            for(var i = 0 ; i < keys.length ; i++) 
                chart_data.push([keys[i], data[keys[i]]]);

            chart_data = google.visualization.arrayToDataTable(chart_data, {});
            var options = {
                chart: {
                    title: 'Top 10 Hashtags'
                },
                hAxis: {
                    title: 'Frequency of Hashtag',
                    minValue: 0,
                },
                vAxis: {
                    title: 'Hashtag'
                },
                bars: 'vertical'
            };
            var chart = new google.charts.Bar(document.getElementById('top10_tab'));
            chart.draw(data, options);
        });
    });

    $.get('/dist/original_fav', function(data) {
        
    });
});