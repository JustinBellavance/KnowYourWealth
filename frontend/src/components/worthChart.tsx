import React from 'react';
import { LinePath, AreaClosed } from '@visx/shape';
import { scaleLinear, scaleTime } from '@visx/scale';
import { timeParse } from 'd3-time-format';
import { Group } from '@visx/group';
import { AxisBottom, AxisLeft } from '@visx/axis';
import { TooltipWithBounds, useTooltip, defaultStyles } from '@visx/tooltip';
import { extent, max } from 'd3-array';
import { localPoint } from '@visx/event';

interface WorthChartProps {
  data: WorthChartData;
}

interface AggregatedDataPoint {
  date: Date;
  value: number;
  sources: string;
}

interface WorthChartData {
  stocks?: { [ticker: string]: { [date: string]: number } };
  real_estate?: { [name: string]: { [date: string]: number } };
  cash?: { [name: string]: { [date: string]: number } };
  debt?: { [name: string]: { [date: string]: number } };
}

const WorthChart: React.FC<WorthChartProps> = ({ data }) => {
  const parseDate = timeParse('%Y-%m-%d');
  const chartWidth = 800;
  const chartHeight = 400;
  const margin = { top: 20, right: 30, bottom: 30, left: 40 };

  const aggregateData = (data: WorthChartData): AggregatedDataPoint[] => {
    const dateMap: { [date: string]: { value: number; sources: string[] } } = {};
    for (const assetType in data) {
      const assetData = data[assetType as keyof WorthChartData];
      if (assetData) {
        for (const asset in assetData) {
          for (const date in assetData[asset]) {
            if (!dateMap[date]) {
              dateMap[date] = { value: 0, sources: [] };
            }
            dateMap[date].value += assetData[asset][date];
            dateMap[date].sources.push(asset);
          }
        }
      }
    }
    return Object.entries(dateMap).map(([date, { value, sources }]) => ({
      date: parseDate(date) || new Date(),
      value,
      sources: sources.join(', '),
    }));
  };

  const aggregatedData = aggregateData(data);

  const xScale = scaleTime({
    domain: extent(aggregatedData, (d) => d.date) as [Date, Date],
    range: [0, chartWidth - margin.left - margin.right],
  });

  const yScale = scaleLinear({
    domain: [0, max(aggregatedData, (d) => d.value) || 0],
    range: [chartHeight - margin.top - margin.bottom, 0],
  });

  const { showTooltip, hideTooltip, tooltipData, tooltipLeft, tooltipTop } = useTooltip<AggregatedDataPoint>();

  return (
    <svg width={chartWidth} height={chartHeight}>
      <Group top={margin.top} left={margin.left}>
        <AxisBottom scale={xScale} top={chartHeight - margin.top - margin.bottom} />
        <AxisLeft scale={yScale} />
        <AreaClosed
          data={aggregatedData}
          x={(d) => xScale(d.date)}
          y={(d) => yScale(d.value)}
          yScale={yScale}
          fill="url(#area-gradient)"
        />
        <LinePath
          data={aggregatedData}
          x={(d) => xScale(d.date)}
          y={(d) => yScale(d.value)}
          stroke="black"
          strokeWidth={2}
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        {aggregatedData.map((d, i) => (
          <circle
            key={i}
            cx={xScale(d.date)}
            cy={yScale(d.value)}
            r={5}
            fill="black"
            onMouseEnter={(event) => {
              const coords = localPoint(event);
              if (coords) {
                showTooltip({
                  tooltipData: d,
                  tooltipLeft: coords.x,
                  tooltipTop: coords.y,
                });
              }
            }}
            onMouseLeave={() => hideTooltip()}
          />
        ))}
        <defs>
          <linearGradient id="area-gradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="rgba(0, 0, 255, 0.3)" />
            <stop offset="100%" stopColor="rgba(0, 0, 255, 0)" />
          </linearGradient>
        </defs>
      </Group>
      {tooltipData && (
        <TooltipWithBounds top={tooltipTop} left={tooltipLeft} style={defaultStyles}>
          <div>Date: {tooltipData.date.toDateString()}</div>
          <div>Value: {tooltipData.value}</div>
          <div>Sources: {tooltipData.sources}</div>
        </TooltipWithBounds>
      )}
    </svg>
  );
};

export default WorthChart;
