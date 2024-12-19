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
    height: 100%;
    padding: 10px;
    background-color: white;
    color: white;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  
  .form-container {
    padding: 10px;
    background-color: white;
    border-color : black;
    border-width: 2px;
    border-radius: 5px;
    margin-left : 10px;
  }
  
  .fade-enter-active, .fade-leave-active {
    transition: opacity 0.5s ease;
  }
  
  .fade-enter, .fade-leave-to {
    opacity: 0;
  }
  </style>
  