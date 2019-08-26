function main() {
  var imagesCommon = ["./image/财税管理.jpg", "./image/企业股权.jpg", "./image/宝宝也可以学的理财课.jpg","./image/创新营销思维.jpg","./image/茶艺文化与健康.png"];

  var root = document.getElementById("root");

  function appendContainer(text) {
    var container = document.createElement("div");
    container.className = "container";

    root.appendChild(container);

    if (text) {
      var introduce = document.createElement("div");
      introduce.className = "introduce";
      var textNode = document.createTextNode(text);
      introduce.appendChild(textNode);
      container.appendChild(introduce);
    }
    return container;
  }

  var fns = [
    function() {
      var text = "";
      var container = appendContainer(text);
      var awesomeSlider = new AwesomeSlider(imagesCommon, container, {
        manual: manual()
      });
    }
  ];

  for (var i = 0; i < fns.length; i++) {
    fns[i]();
  }
}


function manual() {
  var previous = document.createElement("div");
  previous.className = "manual-previous";

  var next = document.createElement("div");
  next.className = "manual-next";

  return {
    previous: previous,
    next: next
  };
}

function readyGo(func) {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", func);
  } else {
    func();
  }
}

readyGo(main);
