$(function () {
  d3.netJsonGraph(
    "./sample-netjson.json", {
      el: "#network-graph",
      metadata: false,
      charge: -250,
      circleRadius: 8,
      labelDy: '-1.8em',
      onClickNode: function (node) {
          console.log("click node!!");
          click_node(node);
      },
      onClickLink: function () {
        console.log("click link!!");
      }
    }
  );
});

var click_node = function (node) {
  $('#nodeInfo').modal('toggle')
}

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
