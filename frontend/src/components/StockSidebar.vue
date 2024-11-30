<template>
    <div class="sidebar">
      <transition name="fade" mode="out-in">
        <div class="form-container">
          <Accordion label="Stocks">
            <StockForm />
          </Accordion>
          <Accordion label="Cash">
            <CashForm />
          </Accordion>
        </div>
      </transition>
    </div>
  </template>
  
  <script setup lang="ts">
  import StockForm from './StockForm.vue';
  import CashForm from './CashForm.vue';
  import Accordion from './Accordion.vue'; // Import the Accordion component
  </script>
  
  <style scoped>
  .sidebar {
    top: 0;
    left: 0;
    width: 300px;
    height: 100%;
    padding: 20px;
    background-color: #2c3e50;
    color: white;
    display: flex;
    flex-direction: column;
    gap: 20px;
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  }
  
  .form-container {
    padding: 20px;
    background-color: #34495e;
    border-radius: 5px;
  }
  
  .fade-enter-active, .fade-leave-active {
    transition: opacity 0.5s ease;
  }
  
  .fade-enter, .fade-leave-to {
    opacity: 0;
  }
  </style>
  