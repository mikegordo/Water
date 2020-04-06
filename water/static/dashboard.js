var loading = false;
var charts = {};
var pots = {};

window.addEventListener("load", function () {
    load_table();
    setInterval(load_table, 5000);
    Chart.defaults.global.legend.display = false;
});

function load_table() {
    if (loading) {
        return;
    }
    loading = true;

    var xhr = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
    xhr.open('POST', '/api');
    xhr.onreadystatechange = function () {
        if (xhr.readyState > 3 && xhr.status == 200) {
            process_data(xhr.responseText);
            loading = false;
        }
    };
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.send();
}

function process_data(data) {
    data = JSON.parse(data);
    document.getElementById("server-time").innerHTML = data.server_time;
    data = data.data;
    document.getElementById("pots-div").innerHTML = '';

    for (var i = 0; i < data.length; i++) {
        document.getElementById("pots-div").appendChild(get_div(data[i]));
    }

    draw_graphs(data);
}

function draw_graphs(d) {
    for (var pot_id in d) {
        let pot = d[pot_id];
        charts[pot.id] = new Chart(document.getElementById('chart_' + pot.id).getContext('2d'), {
            type: "line",
            data: {
                labels: pot.graph_labels,
                datasets: [{
                    data: pot.graph,
                    backgroundColor: 'rgba(0, 0, 0, 1)',
                    borderColor: 'rgba(200, 150, 211, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                animation: {
                    duration: 0
                },
                hover: {
                    animationDuration: 0
                },
                responsiveAnimationDuration: 0,
                scales: {
                    xAxes: [{
                        display: false
                    }]
                }
            }
        });
    }
}

function get_div(pot) {
    var div = document.createElement("div");
    div.className = 'pot';
    div.id = 'pot-' + pot.id;
    var arr = [];
    arr.push('<div class="name">' + pot.name);
    if (pot.online) {
        arr.push('<span class="lamp online"></span>');
    } else {
        arr.push('<span class="lamp offline"></span>');
    }
    arr.push('<span class="id">ID:' + pot.id + '</span>');
    arr.push('</div>');
    arr.push('<div class="description">' + pot.description + '</div>');
    arr.push('<div class="moisture">' + pot.moisture + '%');

    arr.push('<div class="moisture-right">');
    arr.push('<div class="moisture-value">');
    arr.push(pot.moisture_value + '%');
    arr.push('</div>');
    arr.push('<div class="water-value">');
    arr.push(pot.water_value + 's.');
    arr.push('</div>');
    arr.push('</div>');
    arr.push('</div>');
    arr.push('<div class="watering">');
    arr.push('<p>Last watering ');
    if (pot.last_water == null) {
        arr.push('unknown</p>');
    } else {
        arr.push('<strong>' + pot.last_water + '</strong></p>');
    }
    arr.push('<p>');
    for (var i = 0; i < pot.watering.length; i++) {
        if (i > 2) {
            break;
        }
        arr.push(pot.watering[i].created + ' <br/>');
    }
    arr.push('</p>');
    arr.push('<p>');
    if (pot.frequency == null) {
        arr.push('Frequency unknown')
    } else {
        arr.push('Every <strong>' + pot.frequency + '</strong> on average')
    }
    arr.push('</p>');

    arr.push('<canvas id="chart_' + pot.id + '" width="400" height="300"></canvas>');

    arr.push('</div>');
    div.innerHTML = arr.join('\n');
    return div;
}
