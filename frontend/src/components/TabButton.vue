<!-- TabButton.vue -->
<template>
    <button
      :class="['tab-button', { 'active': isActive }]"
      @click="onClick"
    >
      <slot>{{ label }}</slot>
    </button>
  </template>
  
  <script setup lang="ts">
  import { defineProps, defineEmits } from 'vue';
  
  const props = defineProps({
    label: String,
    isActive: Boolean,
  });
  
  const emit = defineEmits(['activate']);
  
  const onClick = () => {
    emit('activate', props.label);
  };
  </script>
  
  <style scoped>
  .tab-button {
    padding: 10px 20px;
    background: none;
    border: 2px solid #34495e;
    color: #34495e;
    font-size: 1.2rem;
    cursor: pointer;
    transition: all 0.3s ease;
    border-radius: 5px;
  }
  
  .tab-button.active {
    background-color: #34495e;
    color: white;
  }
  
  .tab-button:hover {
    background-color: #ecf0f1;
  }
  </style>
  