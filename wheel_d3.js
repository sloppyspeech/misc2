<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>D3.js Circular Progress</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .controls {
            margin-top: 30px;
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            max-width: 400px;
        }
        .control-group {
            display: flex;
            flex-direction: column;
        }
        label {
            font-size: 13px;
            color: #666;
            margin-bottom: 5px;
            font-weight: 500;
        }
        input[type="range"] {
            width: 100%;
        }
        input[type="color"] {
            width: 100%;
            height: 35px;
            border: 1px solid #ddd;
            border-radius: 4px;
            cursor: pointer;
        }
        button {
            grid-column: 1 / -1;
            padding: 12px 24px;
            background: #4a90e2;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
        }
        button:hover {
            background: #357abd;
        }
        .value-display {
            font-size: 12px;
            color: #999;
            margin-top: 3px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div id="progress-chart"></div>
        <div class="controls">
            <div class="control-group">
                <label for="progress">Progress (%)</label>
                <input type="range" id="progress" min="0" max="100" value="30">
                <span class="value-display" id="progress-value">30%</span>
            </div>
            <div class="control-group">
                <label for="progress-color">Progress Color</label>
                <input type="color" id="progress-color" value="#4a90e2">
            </div>
            <div class="control-group">
                <label for="background-color">Background Color</label>
                <input type="color" id="background-color" value="#e0e0e0">
            </div>
            <div class="control-group">
                <label for="text-color">Text Color</label>
                <input type="color" id="text-color" value="#333333">
            </div>
            <button id="download-btn">Download as SVG</button>
        </div>
    </div>

    <script>
        // Configuration
        const width = 200;
        const height = 200;
        const radius = 80;
        const strokeWidth = 20;

        // Create SVG
        const svg = d3.select("#progress-chart")
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .attr("xmlns", "http://www.w3.org/2000/svg");

        const g = svg.append("g")
            .attr("transform", `translate(${width / 2}, ${height / 2})`);

        // Background circle
        const backgroundArc = d3.arc()
            .innerRadius(radius - strokeWidth / 2)
            .outerRadius(radius + strokeWidth / 2)
            .startAngle(0)
            .endAngle(2 * Math.PI);

        const backgroundPath = g.append("path")
            .attr("d", backgroundArc)
            .attr("fill", "#e0e0e0");

        // Progress arc
        const progressArc = d3.arc()
            .innerRadius(radius - strokeWidth / 2)
            .outerRadius(radius + strokeWidth / 2)
            .startAngle(0)
            .cornerRadius(strokeWidth / 2);

        const progressPath = g.append("path")
            .attr("fill", "#4a90e2");

        // Text element
        const text = g.append("text")
            .attr("text-anchor", "middle")
            .attr("dy", "0.35em")
            .style("font-size", "36px")
            .style("font-weight", "600")
            .style("fill", "#333333");

        // Update function
        function updateProgress(progress, progressColor, backgroundColor, textColor) {
            const angle = (progress / 100) * 2 * Math.PI;
            
            backgroundPath
                .transition()
                .duration(300)
                .attr("fill", backgroundColor);
            
            progressPath
                .transition()
                .duration(500)
                .attrTween("d", function() {
                    const interpolate = d3.interpolate(
                        progressPath.attr("data-angle") || 0,
                        angle
                    );
                    return function(t) {
                        const currentAngle = interpolate(t);
                        progressPath.attr("data-angle", currentAngle);
                        return progressArc.endAngle(currentAngle)();
                    };
                })
                .attr("fill", progressColor);
            
            text.transition()
                .duration(500)
                .style("fill", textColor)
                .textTween(function() {
                    const currentValue = parseFloat(text.text()) || 0;
                    const interpolate = d3.interpolate(currentValue, progress);
                    return function(t) {
                        return Math.round(interpolate(t)) + "%";
                    };
                });
        }

        // Event listeners
        const progressInput = document.getElementById("progress");
        const progressColorInput = document.getElementById("progress-color");
        const backgroundColorInput = document.getElementById("background-color");
        const textColorInput = document.getElementById("text-color");
        const progressValueDisplay = document.getElementById("progress-value");
        const downloadBtn = document.getElementById("download-btn");

        function updateChart() {
            const progress = parseInt(progressInput.value);
            const progressColor = progressColorInput.value;
            const backgroundColor = backgroundColorInput.value;
            const textColor = textColorInput.value;
            
            progressValueDisplay.textContent = progress + "%";
            updateProgress(progress, progressColor, backgroundColor, textColor);
        }

        progressInput.addEventListener("input", updateChart);
        progressColorInput.addEventListener("input", updateChart);
        backgroundColorInput.addEventListener("input", updateChart);
        textColorInput.addEventListener("input", updateChart);

        // Download function
        downloadBtn.addEventListener("click", function() {
            const svgElement = document.querySelector("#progress-chart svg");
            const svgData = new XMLSerializer().serializeToString(svgElement);
            const blob = new Blob([svgData], { type: "image/svg+xml" });
            const url = URL.createObjectURL(blob);
            
            const link = document.createElement("a");
            link.href = url;
            link.download = "circular-progress.svg";
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
        });

        // Initialize
        updateProgress(30, "#4a90e2", "#e0e0e0", "#333333");
    </script>
</body>
</html>
