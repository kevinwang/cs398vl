var data;

function main() {
    console.log("JS file loaded!");
    d3.json('data/data.json', function(data) {
        data = _.map(data, function(elem) {
            return {word: elem.word, slope: elem.slope, freqs: elem.freqs, ch: elem.ch};
        });
        window.data = data;
        barChart("#main", data);
        displayWord(0);
    });
}

function barChart(id, data) {
    var margin = {top: 30, right: 10, bottom: 10, left: 10},
        width = $(id).width() || 960 - margin.left - margin.right,
        height = $(id).height() || 800 - margin.top - margin.bottom;

    var x = d3.scale.linear()
        .domain(d3.extent(data, function(d) { return d.slope; }))
        .range([100, width - 100]);

    var y = d3.scale.ordinal()
        .domain(data.map(function(d) { return d.word; }))
        .rangeRoundBands([0, height], .2);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("top");

    var svg = d3.select(id).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg.selectAll(".bar")
        .data(data)
        .enter().append("rect")
        .attr("class", function(d) { return d.slope < 0 ? "bar negative" : "bar positive"; })
        .attr("x", function(d) { return x(Math.min(0, d.slope)); })
        .attr("y", function(d) { return y(d.word); })
        .attr("width", function(d) { return Math.abs(x(d.slope) - x(0)); })
        .attr("height", y.rangeBand())
        .on("click", function(d, i) {
            displayWord(i);
        });

    svg.selectAll("text.left")
        .data(_.map(data, function(elem) { return elem.word; }))
        .enter().append("text")
        .attr("x", 100)
        .attr("y", function(d) { return y(d) + y.rangeBand()/2; })
        .attr("dx", -5)
        .attr("dy", ".36em")
        .attr("text-anchor", "end")
        .attr("class", "word")
        .text(String)
        .on("click", function(d, i) {
            displayWord(i);
        });

    svg.selectAll("text.right")
        .data(_.map(data, function(elem) { return elem.word; }))
        .enter().append("text")
        .attr("x", width-90)
        .attr("y", function(d) { return y(d) + y.rangeBand()/2; })
        .attr("dx", -5)
        .attr("dy", ".36em")
        .attr("text-anchor", "start")
        .attr("class", "word")
        .text(String)
        .on("click", function(d, i) {
            displayWord(i);
        });

    svg.append("g")
        .attr("class", "x axis")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .append("line")
        .attr("x1", x(0))
        .attr("x2", x(0))
        .attr("y2", height);
}

function lineChart(id, data) {
    console.log(data);
    var margin = {top: 30, right: 10, bottom: 20, left: 50},
        width = $(id).width() || 960 - margin.left - margin.right,
        height = $(id).height() || 300 - margin.top - margin.bottom;

    var x = d3.scale.linear()
        .domain(d3.extent(data, function(d) { return d.ch; }))
        .range([0, width - 55]);

    var y = d3.scale.linear()
        .domain([0, d3.max(data, function(d) { return d.freq; })])
        .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom")
        .tickValues([1, 2, 3, 4]);

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    var line = d3.svg.line()
        .interpolate("monotone")
        .x(function(d) { return x(d.ch); })
        .y(function(d) { return y(d.freq); });

    var svg = d3.select(id).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Relative frequency in chapter");

    svg.append("path")
        .datum(data)
        .attr("class", "line")
        .attr("d", line);
}

function displayWord(i) {
    d3.select("#line > svg").remove();
    lineChart("#line", data[i].freqs);
    $('#word').text(data[i].word);
}
