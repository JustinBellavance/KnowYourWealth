<template>
    <div class="accordion">
      <div class="accordion-header" @click="toggleAccordion">
        <span>{{ label }}</span>
        <button class="accordion-toggle-btn">
          <span v-if="isOpen">▼</span>
          <span v-else>▶︎</span>
        </button>
      </div>
      <div v-show="isOpen" class="accordion-body" @click.stop>
        <slot></slot>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue';
  
  const props = defineProps({
    label: String, // The label for the accordion header
  });
  
  const isOpen = ref(false);
  
  const toggleAccordion = () => {
    isOpen.value = !isOpen.value;
  };
  </script>
  
  <style scoped>
.accordion {
  margin-bottom: 10px;

}

.accordion-item {
  border: 1px solid #ecf0f1;
  border-radius: 5px;
  margin-bottom: 5px;
  background-color: #34495e;
}

.accordion-header {
  padding: 10px;
  color: black;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 24px;
}

.accordion-body {
  padding: 15px;
  background-color: #2c3e50;
}
.accordion-toggle-btn {
  margin-left : 10px;
}

.accordion-item.is-open .accordion-header {
  background-color: #1abc9c;
}

.icon {
  transition: transform 0.3s ease;
}

.icon.is-open {
  transform: rotate(180deg);
}
  </style>
  