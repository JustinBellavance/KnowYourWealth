<template>
    <div class="card" @click="toggleExpand" :class="{ expanded: isExpanded }">
      <div class="card-header">
        <p>{{ asset.title }}</p>
        <p class="value">{{ cadConvert(asset.value) }}</p>
      </div>
      
      <!-- Expanded Content -->
      <transition name="expand">
        <div v-if="isExpanded" class="expanded-content">
          <!-- Table for displaying asset details -->
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Quantity</th>
                <th>Price</th>
                <th>Value</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(value, key) in asset.details" :key="key">
                <td>{{ value.name }}</td>
                <td>{{ value.quantity }}</td>
                <td>{{ cadConvert(value.price) }}</td>
                <td>{{ cadConvert(value.value) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </transition>
    </div>
  </template>
  
  <script lang="ts" setup>
  import { ref } from "vue";
  
  interface assetDetails {
    [key: string]: string | number;
  }
  
  interface Asset {
    title: string;
    value: string;
    details: assetDetails;
  }
  
  defineProps<{
    asset: Asset;
  }>();
  
  const isExpanded = ref(false);
  
  // Toggle the expanded state of the card
  const toggleExpand = () => {
    isExpanded.value = !isExpanded.value;
  };
  
  const cadConvert = (number: number) => {
    return Intl.NumberFormat("en-CA", { style: "currency", currency: "CAD" }).format(number);
  };
  </script>
  
  <style scoped>
  .card {
    border: 1px solid #ccc;
    padding: 20px;
    margin: 10px;
    cursor: pointer;
    transition: all 0.3s ease;
    width: 100%;
  }
  
  .card.expanded {
    background-color: #f0f0f0;
    width: 100%;
    margin-bottom: 20px;
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: x-large;
  }
  
  .value {
    text-align: right;
  }
  
  .expanded-content {
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px solid #ccc;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
  }
  
  th,
  td {
    padding: 8px;
    text-align: left;
    border-bottom: 1px solid #ddd;
  }
  
  th {
    background-color: #f2f2f2;
  }
  
  .transition-expand-enter-active,
  .transition-expand-leave-active {
    transition: height 0.3s ease;
  }
  
  .transition-expand-enter,
  .transition-expand-leave-to {
    height: 0;
    overflow: hidden;
  }
  </style>
  