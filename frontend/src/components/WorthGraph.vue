<template>
  <div class="graph-container" ref="graphContainer">
    <svg ref="svgRef"></svg>
    <div ref="tooltipRef" class="tooltip" style="display: none;"></div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import * as d3 from "d3";

// Props for data and dimensions
const props = defineProps<{
  data: { date: string; value: number; name: string }[];
  width?: number;
  height?: number;
}>();

const defaultWidth = props.width || 800;
const defaultHeight = props.height || 400;

// D3.js rendering logic
const svgRef = ref<SVGSVGElement | null>(null);
const tooltipRef = ref<HTMLDivElement | null>(null);

onMounted(() => {
  if (props.data.length > 0) renderGraph();
});

const renderGraph = () => {
  if (!svgRef.value || !tooltipRef.value) return;

  const tooltip = d3.select(tooltipRef.value);
  d3.select(svgRef.value).selectAll("*").remove();

  const margin = { top: 20, right: 30, bottom: 80, left: 80 };
  const width = defaultWidth - margin.left - margin.right;
  const height = defaultHeight - margin.top - margin.bottom;

  const svg = d3
    .select(svgRef.value)
    .attr("width", defaultWidth)
    .attr("height", defaultHeight)
    .append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

  // Parse date as "YYYY-MM-DD"
  const parseDate = d3.timeParse("%Y-%m-%d");
  const formatDate = d3.timeFormat("%Y-%m-%d");

  // Map and ensure dates are parsed without time
  const assetData = props.data.map(d => ({
    date: parseDate(d.date),
    value: d.value,
    name: d.name,
  }));

  // Group data by date
  const groupedData = Array.from(
    d3.group(assetData, d => formatDate(d.date || new Date())), // Use formatted date as key
    ([date, values]) => {
      const entry: Record<string, number | string | Date > = { date: parseDate(date) || new Date() }; // Convert date back to Date object
      values.forEach(v => {
        entry[v.name] = v.value;
      });
      return entry;
    }
  );

  const names = Array.from(new Set(assetData.map(d => d.name)));

  // Create stack
  const stack = d3
    .stack()
    .keys(names)
    .value((d, key) => d[key] || 0);

  const stackedData = stack(groupedData);

  // Scales
  const xScale = d3
    .scaleTime()
    .domain(d3.extent(assetData, d => d.date) as [Date, Date])
    .range([0, width]);


    const yScale = d3
      .scaleLinear()
      .domain([0, d3.max(stackedData.flatMap(layer => layer.map(d => d[1])))!])
      .range([height, 0]);

  const colorScale = d3
    .scaleOrdinal(d3.schemeDark2) // A softer, pastel color palette
    .domain(names);

  // Axes
  const xAxis = d3.axisBottom(xScale)
  .tickFormat(d => d3.timeFormat("%b %d")(new Date(d))) // Convert timestamp to Date before formatting
  .ticks(6);
  
  const yAxis = d3.axisLeft(yScale).ticks(6).tickSize(0).tickFormat(d3.format("$,.0f")); // Format as dollar with commas for thousands

  svg
    .append("g")
    .attr("transform", `translate(0, ${height})`)
    .call(xAxis)
    .selectAll("text")
    .attr("transform", "rotate(-45)")
    .style("text-anchor", "end")
    .style("font-size", "20px")
    .style("color", "black")

  svg
    .append("g")
    .call(yAxis)
    .selectAll("text")
    .style("font-size", "20px")
    .style("color", "black")

  // Draw stacked areas with a smooth curve
  const area = d3
    .area()
    .x(d => xScale((d.data as any).date))
    .y0(d => yScale(d[0]))
    .y1(d => yScale(d[1]))
    .curve(d3.curveMonotoneX); // Smoother curves

    const hoverLine = svg.append("line").style("stroke", "#333").style("stroke-width", 2).style("visibility", "hidden");


  svg
    .selectAll(".layer")
    .data(stackedData)
    .enter()
    .append("path")
    .attr("class", "layer")
    .attr("d", area)
    .style("fill", (_, i) => colorScale(names[i]) as string)
    .style("opacity", 0.8)
    .style("stroke", "#000") // Set the stroke color to black for the curve lines
    .style("stroke-width", "1px") // Optional: Set stroke width for better visibility
    .on("mouseover", (_, layer) => {
      tooltip.style("display", "block");
    })
    .on("mousemove", (event, layer) => {
      const [x] = d3.pointer(event);
      const hoveredDate = xScale.invert(x); // Returns a Date object

      // Show vertical line at the hovered x position
      hoverLine
        .attr("x1", x)
        .attr("x2", x)
        .attr("y1", 0)
        .attr("y2", height)
        .style("visibility", "visible");

      const formattedDate = formatDate(hoveredDate); // Format it to "YYYY-MM-DD"

      // Gather all the data for the hovered date
      const tooltipData = stackedData.map(layer => {
        const dataPoint = layer.find(d => formatDate(d.data.date) === formattedDate);
        const value = dataPoint ? dataPoint[1] - dataPoint[0] : 0;
        return { name: layer.key, value };
      });

      // Display all information in the tooltip
      tooltip
        .style("display", "block")
        .html(
          tooltipData.reverse().map(d => `${d.name}: $${d.value.toFixed(2)}`).join("<br>")
        )
        .style("left", `${event.pageX - 400}px`)
        .style("top", `${event.pageY - 300}px`);
    })
    .on("mouseout", () => {
      hoverLine.style("visibility", "hidden");
      tooltip.style("display", "none");
    });
};

// Watch for data updates to re-render the graph
watch(() => props.data, renderGraph, { deep: true });
</script>

<style scoped>
.graph-container {
  position: relative;
  font-family: 'Arial', sans-serif; /* Modern font */
}

.tooltip {
  position: absolute;
  background-color: rgba(44, 62, 80, 0.8); /* Transparent dark background */
  color: white;
  padding: 10px;
  pointer-events: none;
  font-size: 18px;
  white-space: nowrap;
}

path.layer {
  transition: all 0.3s ease;
}
</style>
