// This is a proof of concept for Planman. All we want to do is draw
// a couple of rectangles on screen. I'm going to follow the structure
// of backbone.js.


(function() {

    var root = this;

    // This sets up a Planman variable in the root namespace
    var Planman;
    if (typeof exports !== 'undefined') {
        Planman = exports;
    }
    else {
        Planman = root.Planman = {};
    }


    // # Support functions
    // Creates an svg node. The `svgType` should be things like `svg`, `rect`, etc.
    // See [SVG Shapes](http://www.w3.org/TR/SVG11/shapes.html) for more info.
    function newSvgNode(svgType) {
        var result = document.createElementNS("http://www.w3.org/2000/svg", svgType);
        return result;
    }

    // # Main functions
    Planman.init = function() {
        Planman.viewer = document.getElementById("viewer");
        Planman.svgViewer = newSvgNode("svg");
        Planman.viewer.appendChild(Planman.svgViewer);
    }

    Planman.addRectangle = function(x, y, width, height, color) {
        var result = newSvgNode("rect");
        result.x.baseVal.value = x;
        result.y.baseVal.value = y;
        result.width.baseVal.value = width;
        result.height.baseVal.value = height;
        result.style.fill = color;
        Planman.svgViewer.appendChild(result);
        return result;
    }
}).call(this);

