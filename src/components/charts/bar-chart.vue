<script setup>
import { BarChart } from "vue-chart-3";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

const props = defineProps({
  initialData: { type: Object, required: true, default: {} },
});

const chartData = props.initialData.value;
const options = props.initialData.option;
const styles = props.initialData.styles;
</script>

<template>
  <BarChart :chartData="chartData" :options="options" :style="styles" />
</template>
