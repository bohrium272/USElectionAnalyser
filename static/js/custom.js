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
        var html = '';
        for(var i = 0 ; i < data.length ; i++)
            html += '<li class="mdl-list__item"><span class="mdl-list__item-primary-content">#' + data[i] + '</span></li>';
        document.getElementById('top10_list').innerHTML = html;
        console.log();
        ;
        ;
        ;
        ;
        ;
        ;
        ;
        ;
        
    });
});