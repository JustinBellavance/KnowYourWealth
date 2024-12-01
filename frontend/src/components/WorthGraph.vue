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

    const margin = { top: 20, right: 30, bottom: 50, left: 50 };
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
    const data = props.data.map(d => ({
      date: parseDate(d.date),
      value: d.value,
      name: d.name,
    }));

    // Group data by date
    const groupedData = Array.from(
      d3.group(data, d => formatDate(d.date)), // Use formatted date as key
      ([date, values]) => {
        const entry: Record<string, number | string> = { date: parseDate(date) }; // Convert date back to Date object
        values.forEach(v => {
          entry[v.name] = v.value;
        });
        return entry;
      }
    );

    const names = Array.from(new Set(data.map(d => d.name)));

    // Create stack
    const stack = d3
      .stack()
      .keys(names)
      .value((d, key) => d[key] || 0);

    const stackedData = stack(groupedData);

    // Scales
    const xScale = d3
      .scaleTime()
      .domain(d3.extent(data, d => d.date) as [Date, Date])
      .range([0, width]);

    const yScale = d3
      .scaleLinear()
      .domain([0, d3.max(stackedData.flatMap(layer => layer.map(d => d[1])))!])
      .range([height, 0]);

    const colorScale = d3
      .scaleOrdinal(d3.schemeCategory10)
      .domain(names);

    // Axes
    const xAxis = d3.axisBottom(xScale).tickFormat(d3.timeFormat("%b %d"));
    const yAxis = d3.axisLeft(yScale).ticks(6);

    svg
      .append("g")
      .attr("transform", `translate(0, ${height})`)
      .call(xAxis)
      .selectAll("text")
      .attr("transform", "rotate(-45)")
      .style("text-anchor", "end");

    svg.append("g").call(yAxis);

    // Draw stacked areas
    const area = d3
      .area()
      .x(d => xScale((d.data as any).date))
      .y0(d => yScale(d[0]))
      .y1(d => yScale(d[1]))
      .curve(d3.curveMonotoneX);

    svg
      .selectAll(".layer")
      .data(stackedData)
      .enter()
      .append("path")
      .attr("class", "layer")
      .attr("d", area)
      .style("fill", (_, i) => colorScale(names[i]) as string)
      .style("opacity", 0.8)
      .on("mouseover", (_, layer) => {
        tooltip.style("display", "block");
      })
      .on("mousemove", (event, layer) => {
        const [x] = d3.pointer(event);
        const hoveredDate = xScale.invert(x); // Returns a Date object
        const formattedDate = formatDate(hoveredDate); // Format it to "YYYY-MM-DD"

        const name = layer.key || "";
        const dataPoint = layer.find(d => formatDate(d.data.date) === formattedDate); // Compare using formatted date
        const value = dataPoint ? dataPoint.data[layer.key] : 0;

        tooltip
          .html(`${name}<br>${formattedDate}<br>$${value}`)
          .style("left", `${event.pageX - 300}px`)
          .style("top", `${event.pageY - 300}px`);
      })
      .on("mouseout", () => {
        tooltip.style("display", "none");
      });
  };
  
  // Watch for data updates to re-render the graph
  watch(() => props.data, renderGraph, { deep: true });
  </script>
  
  <style scoped>
  .graph-container {
    position: relative;
  }
  
  .tooltip {
    position: absolute;
    background-color: #2c3e50;
    color: white;
    padding: 8px;
    border-radius: 4px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    pointer-events: none;
    font-size: 0.9rem;
    white-space: nowrap;
  }
  </style>
  