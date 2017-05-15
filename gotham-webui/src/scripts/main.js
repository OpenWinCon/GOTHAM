$(function () {
  d3.netJsonGraph(
    "https://raw.githubusercontent.com/netjson/netjsongraph.js/master/examples/data/netjson.json", {
      el: "#network-graph",
      metadata: false,
      charge: -250,
      circleRadius: 8,
      labelDy: '-1.8em',
      onClickNode: function (node) {
          console.log("click node!!");
          console.log(node);
      },
      onClickLink: function () {
        console.log("click link!!");
      }
    }
  );
});

var search_node = function () {
  var name = $("#search").val();
  if(name.length == 0) {
    $("#network-graph").removeClass("focusing");
    $(".njg-node").removeClass("focused");
  } else {
    $("#network-graph").addClass("focusing");
    node[0].forEach(function (x, i) {
      data = x.__data__;
      if(data.id.includes(name)) {
        $(x).addClass("focused");
      } else {
        $(x).removeClass("focused");
      }
    });
  }
}
