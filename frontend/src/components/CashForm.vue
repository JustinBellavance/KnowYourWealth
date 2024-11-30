<template>
    <div class="form">
      <div class="tab-buttons">
        <button
          :class="{ active: isAdding }"
          @click="setAction('add')"
        >
          Add
        </button>
        <button
          :class="{ active: !isAdding }"
          @click="setAction('remove')"
        >
          Remove
        </button>
      </div>
  
      <div class="form-group">
        <label for="amount">{{ isAdding ? 'Amount to Add' : 'Amount to Remove' }}</label>
        <input
          type="number"
          id="amount"
          v-model="amount"
          placeholder="Enter amount"
          min="1"
        />
      </div>
      <div class="form-group">
        <label for="date">Date</label>
        <input type="date" id="date" v-model="date" />
      </div>
      <button @click="submitCash">
        {{ isAdding ? 'Submit Add' : 'Submit Remove' }}
      </button>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from "vue";
  
  const amount = ref<number | null>(null);
  const date = ref<string>(new Date().toISOString().split("T")[0]); // Default to current date
  const isAdding = ref(true); // Tracks whether the action is 'Add' or 'Remove'
  
  // Function to set the action type (Add or Remove)
  const setAction = (action: "add" | "remove") => {
    isAdding.value = action === "add";
  };
  
  // Dummy submit function for backend integration
  const submitCash = () => {
    if (!amount.value || !date.value) {
      alert("Please fill in all fields.");
      return;
    }
  
    const cashAction = {
      action: isAdding.value ? "add" : "remove",
      amount: amount.value,
      date: date.value,
    };
  
    console.log("Cash action submitted:", cashAction);
    // Here, you would differentiate backend routes based on cashAction.action
    // e.g., POST to `/cash/add` or `/cash/remove`
  };
  </script>
  
  <style scoped>
  .form {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  
  .tab-buttons {
    display: flex;
    gap: 10px;
    margin-bottom: 15px;
  }
  
  .tab-buttons button {
    padding: 8px 16px;
    border-radius: 5px;
    border: 1px solid #ecf0f1;
    background-color: #34495e;
    color: white;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s, color 0.3s;
  }
  
  .tab-buttons button.active {
    background-color: #3498db;
    color: white;
  }
  
  .tab-buttons button:hover {
    background-color: #2c3e50;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
  }
  
  label {
    margin-bottom: 5px;
    font-weight: bold;
    color: #ecf0f1;
  }
  
  input {
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #ecf0f1;
    background-color: #2c3e50;
    color: white;
  }
  
  input::placeholder {
    color: #bdc3c7;
  }
  
  button {
    padding: 10px;
    background-color: #27ae60;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: bold;
    transition: background-color 0.3s;
  }
  
  button:hover {
    background-color: #2ecc71;
  }
  </style>
  