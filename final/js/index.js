var data;

function main() {
    wordCountChart("#wc");
    percentEnglish('#eng_fw', 0);
    percentEnglish('#eng_ul', 1);
    percentEnglish('#eng_ofk', 2);
    $('#novelty').load('data/novelty.html');
}

function wordCountChart(id) {
    var margin = {top: 20, right: 20, bottom: 30, left: 40},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    var x0 = d3.scale.ordinal()
        .rangeRoundBands([0, width], .1);

    var x1 = d3.scale.ordinal();

    var y = d3.scale.linear()
        .range([height, 0]);

    var color = d3.scale.ordinal()
        .range(["#98abc5", "#8a89a6"]);

    var xAxis = d3.svg.axis()
        .scale(x0)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .tickFormat(d3.format(".2s"));

    var svg = d3.select(id).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    d3.csv("data/wc.csv", function(error, data) {
        var countNames = d3.keys(data[0]).filter(function(key) { return key !== "Title"; });

        data.forEach(function(d) {
            d.counts = countNames.map(function(name) { return {name: name, value: +d[name]}; });
        });

        x0.domain(data.map(function(d) { return d.Title; }));
        x1.domain(countNames).rangeRoundBands([0, x0.rangeBand()]);
        y.domain([0, d3.max(data, function(d) { return d3.max(d.counts, function(d) { return d.value; }); })]);

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
        .text("Number of words");

    var state = svg.selectAll(".state")
        .data(data)
        .enter().append("g")
        .attr("class", "g")
        .attr("transform", function(d) { return "translate(" + x0(d.Title) + ",0)"; });

    state.selectAll("rect")
        .data(function(d) { return d.counts; })
        .enter().append("rect")
        .attr("width", x1.rangeBand())
        .attr("x", function(d) { return x1(d.name); })
        .attr("y", function(d) { return y(d.value); })
        .attr("height", function(d) { return height - y(d.value); })
        .style("fill", function(d) { return color(d.name); });

    var legend = svg.selectAll(".legend")
        .data(countNames.slice())
        .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

    legend.append("rect")
        .attr("x", width - 18)
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", color);

    legend.append("text")
        .attr("x", width - 24)
        .attr("y", 9)
        .attr("dy", ".35em")
        .style("text-anchor", "end")
        .text(function(d) { return d; });

    });
}

function percentEnglish(id, idx) {
    var width = 250,
        height = 250,
        radius = Math.min(width, height) / 2;

    var color = d3.scale.ordinal()
        .range(["#d0743c", "#a05d56"]);

    var arc = d3.svg.arc()
        .outerRadius(radius - 10)
        .innerRadius(0);

    var pie = d3.layout.pie()
        .sort(null)
        .value(function(d) { return d.percent; });

    var svg = d3.select(id).append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    d3.json("data/english.json", function(error, data) {

        data[idx].sects.forEach(function(d) {
            d.name = d.name;
            d.percent = +d.percent;
        });

        var g = svg.selectAll(".arc")
        .data(pie(data[idx].sects))
        .enter().append("g")
        .attr("class", "arc");

    g.append("path")
        .attr("d", arc)
        .style("fill", function(d) { return color(d.data.name); });

    });
}

main();
