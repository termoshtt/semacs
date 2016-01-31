
var w = 1200, h = 600, fill = d3.scale.category20();
var r = 5;

var vis = d3.select("#chart")
  .append("svg:svg")
  .attr("width", w)
  .attr("height", h)
  ;

var info = d3.select("#info")
  .append("p")
  ;

d3.json("/json", function(json) {
  var force = d3.layout.force()
    .charge(-40)
    .linkDistance(40)
    .nodes(json.nodes)
    .links(json.links)
    .size([w, h])
    .start();

  var link = vis.selectAll("line.link")
    .data(json.links)
    .enter().append("svg:line")
    .attr("class", "link")
    .style("stroke-width", function(d) { return Math.sqrt(d.value); })
    .attr("x1", function(d) { return d.source.x; })
    .attr("y1", function(d) { return d.source.y; })
    .attr("x2", function(d) { return d.target.x; })
    .attr("y2", function(d) { return d.target.y; });

  var node = vis.selectAll("circle.node")
    .data(json.nodes)
    .enter().append("svg:circle")
    .attr("class", function(d) { return d.type; })
    .attr("cx", function(d) { return d.x; })
    .attr("cy", function(d) { return d.y; })
    .attr("r", function(d){ return r; })
    .call(force.drag)
    .on("click", function(d, i){ info.text(d.path); })
    ;

  node.append("svg:title")
    .text(function(d) { return d.name; });

  vis.style("opacity", 1e-6)
    .transition()
    .duration(1000)
    .style("opacity", 1);

  var band = function (max_val, x) { return Math.min(max_val-r, Math.max(r, x)); };

  force.on("tick", function() {
    link
      .attr("x1", function(d) { return band(w, d.source.x); })
      .attr("y1", function(d) { return band(h, d.source.y); })
      .attr("x2", function(d) { return band(w, d.target.x); })
      .attr("y2", function(d) { return band(h, d.target.y); });

    node
      .attr("cx", function(d) { return band(w, d.x); })
      .attr("cy", function(d) { return band(h, d.y); });
  });
});
