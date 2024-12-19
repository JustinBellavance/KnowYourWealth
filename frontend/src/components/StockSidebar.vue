<template>
    <div class="sidebar">
      <transition name="fade" mode="out-in">
        <div class="form-container">
          <Accordion label="Stocks">
            <StockForm @update-data="refreshData"/>
          </Accordion>
          <Accordion label="Cash">
            <CashForm @update-data="refreshData"/>
          </Accordion>
        </div>
      </transition>
    </div>
  </template>
  
  <script setup lang="ts">
  import {defineEmits} from "vue";

  import StockForm from './StockForm.vue';
  import CashForm from './CashForm.vue';
  import Accordion from './Accordion.vue'; 

  const emit = defineEmits(['update-data']);

  const updateData = () => {
    emit('update-data'); // Emit the event
  };

  function refreshData(){
    updateData();
  }

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
    max-width : 250px;
    min-width: 250px;
    margin-left : 2.5px;
  }
  
  .form-container {
    padding: 10px;
    background-color: white;
    margin-left : 10px;
  }
  
  .fade-enter-active, .fade-leave-active {
    transition: opacity 0.5s ease;
  }
  
  .fade-enter, .fade-leave-to {
    opacity: 0;
  }
  </style>
  