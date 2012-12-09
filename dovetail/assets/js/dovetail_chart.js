
function DovetailChart(viewerId) {
    // Creates an svg node. The `svgType` should be things like `svg`, `rect`, etc.
    // See [SVG Shapes](http://www.w3.org/TR/SVG11/shapes.html) for more info.
    function createSvgNode(svgType) {
        var result = document.createElementNS("http://www.w3.org/2000/svg", svgType);
        return result;
    }

    // Initialization
    var viewerElement = document.getElementById(viewerId);
    var svgViewer = createSvgNode('svg');
    viewerElement.appendChild(svgViewer);

    function addRectangle(x, y, width, height, color) {
        var result = createSvgNode("rect");
        result.x.baseVal.value = x;
        result.y.baseVal.value = y;
        result.width.baseVal.value = width;
        result.height.baseVal.value = height;
        result.style.fill = color;
        svgViewer.appendChild(result);
        return result;
    }

    function renderData(data) {
        data.rows.forEach(function(r) {
            r.bars.forEach(function(b) {
                addRectangle(b.x, b.y, b.width, b.height, b.color);
            });
        });
    }


    var result = {
        addRectangle: addRectangle,
        renderData: renderData
    };

    return result;
}
