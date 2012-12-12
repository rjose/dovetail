
function DovetailChart(viewerId, data, auxData) {
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
    var data = data;
    var auxData = auxData;
    var popover = null;

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

   function hidePopover() {
       if (popover) {
          popover.remove();
       }
   }

   function showPopover(x, y, itemId) {
       hidePopover();
       if (!auxData) {
          return;
       }

       popover = $(document.createElement('div'));
       popover.addClass('popover fade bottom in');

       var popoverInner = $(document.createElement('div'));
       popoverInner.addClass('popover-inner');

       var title = $(document.createElement('h3'));
       title.addClass('popover-title');
       title.html(auxData[itemId].title);

       var content = $(document.createElement('div'));
       content.addClass('popover-content');
       content.html(auxData[itemId].content);

       popoverInner.append(title);
       popoverInner.append(content);

       popover.append(popoverInner);

       // TODO: Send this ID in
       var chart = $('#timeline-chart');
       var chartX = chart[0].offsetLeft;
       var chartY = chart[0].offsetTop;
       y += chartY;
       x = x + chartX;
       popover.attr('style', 'top: ' + y + 'px; left: ' + x + 'px; display: block;');
       $('#timeline-chart').append(popover);

       popover.click(function () {
          hidePopover();
       })
   }

    function renderData() {
        // Set chart height from data
        chartHeight = data.chart_height;
        svgViewer.setAttribute('height', chartHeight);

        data.rows.forEach(function(r) {
            var textX = 10;
            var textY = r.y + 15;
            addText(textX, textY, r.label, '#333');

            r.bars.forEach(function(b) {
                var rect = addRectangle(b.x, r.y, b.width, b.height, b.color);
                rect.onclick = function(event) {
                    showPopover(event.offsetX, event.offsetY, b.id);
                }
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
