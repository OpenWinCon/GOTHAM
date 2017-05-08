$(function () {
  d3.netJsonGraph(
    "https://raw.githubusercontent.com/netjson/netjsongraph.js/master/examples/data/netjson.json", {
      el: "#network-graph",
      metadata: false,
      charge: -250,
      circleRadius: 8,
      labelDy: '-1.8em',
    }
  );
});
