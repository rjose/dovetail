
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
    var chartHeight = svgViewer.getAttribute('height');
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

   function addText(x, y, text, color) {
       var result = createSvgNode("text");
       result.setAttributeNS(null, "x", x);
       result.setAttributeNS(null, "y", y);
       result.setAttributeNS(null, "fill", color);

       var textNode = document.createTextNode(text);
       result.appendChild(textNode);

       svgViewer.appendChild(result);
       return result;
   }
   
   function addLine(x1, y1, x2, y2, color) {
       var result = createSvgNode("line");
        result.x1.baseVal.value = x1;
        result.y1.baseVal.value = y1;
        result.x2.baseVal.value = x2;
        result.y2.baseVal.value = y2;
        result.style.stroke = color;
        svgViewer.appendChild(result);

       return result;
   }

    function renderData(data) {
        // Set chart height from data
        chartHeight = data.chart_height;
        svgViewer.setAttribute('height', chartHeight);

        data.rows.forEach(function(r) {
            var textX = 10;
            var textY = r.y + 15;
            addText(textX, textY, r.label, '#333');

            r.bars.forEach(function(b) {
                addRectangle(b.x, r.y, b.width, b.height, b.color);
            });
        });
        data.dates.forEach(function(d) {
            // Add lines going across chart
            addLine(d.x, 0, d.x, chartHeight, 'gray');
            
            // Add labels
            var textX = d.x + 4;
            var textY = 10;
            if (chartHeight > 400) {
                addText(textX, textY, d.label, '#333');
            }
            addText(textX, chartHeight, d.label, '#333');
        });
    }


    var result = {
        addRectangle: addRectangle,
        addText: addText,
        renderData: renderData
    };

    return result;
}
