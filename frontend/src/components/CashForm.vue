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
        <label for="name">Name (optional)</label>
        <input
          type="text"
          id="name"
          v-model="name"
          placeholder="e.g., HISA"
          maxlength="10"
        />
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
        <label for="interest">Interest % (Annualized)</label>
        <input type="interest" id="interest" placeholder="%0" min="0" v-model="interest" />
      </div>
      <div class="form-group">
        <label for="date">Date</label>
        <input type="date" id="date" v-model="date" />
        <div>
        </div>
      </div>
      <button @click="confirmCash">
        {{ isAdding ? 'Submit Add' : 'Submit Remove' }}
      </button>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from "vue";
  import {useRoute} from "vue-router"
  import axios from "axios"

  const route = useRoute();
  const portfolioId = route.params.id; // Access the `id` from the URL
  
  const amount = ref<number | null>(null);
  const name = ref<string | null>(null);
  const date = ref<string>( new Date().toLocaleDateString("en-CA").split("T")[0]); // Default to current date
  const interest = ref<number>(0);
  
  const isAdding = ref(true); // Tracks whether the action is 'Add' or 'Remove'

  const apiUrl = import.meta.env.VITE_API_URL;
  
  // Function to set the action type (Add or Remove)
  const setAction = (action: "add" | "remove") => {
    isAdding.value = action === "add";
  };

  const clearForm = () => {
    name.value = "";
    amount.value = 0;
    date.value = new Date().toLocaleDateString("en-CA").split("T")[0];
    interest.value = 0;
  };
  
  // Dummy submit function for backend integration
  const confirmCash = () => {
    if (!amount.value || !date.value) {
      alert("Please fill in all fields.");
      return;
    }
  
    const cashAction = {
      action: isAdding.value ? "add" : "remove",
      name : name.value,
      amount: amount.value,
      date: date.value,
      interest: interest.value,
    };

    const isConfirmed = confirm(`
        Please confirm the following details:
        Name: ${cashAction.name}
        Action: ${cashAction.action.toUpperCase()}
        Amount: $${cashAction.amount.toFixed(2)}
        Interest (Annualized) : %${cashAction.interest}
        Date: ${cashAction.date}
    `);

    if (isConfirmed) {
      console.log("Cash transaction:", cashAction);

      let url = `${apiUrl}/cash/add/${portfolioId}`;

      if (cashAction.action === 'remove'){
        url = `${apiUrl}/cash/remove/${portfolioId}`;
      }

      axios.put(url, cashAction)
      .then(response => {
        console.log('Response:', response.data);
      })
      .catch(error => {
        if (error.response) {
          // Server responded with a status outside the 2xx range
          console.error('Error status:', error.response.status);
          console.error('Error details:', error.response.data);
          
          // Show an alert to the user
          alert(`Error: ${error.response.data.deta || 'Something went wrong. Please try again later.'} Status Code: ${error.response.status}`);

        } else {
          console.error('Error:', error);
        }
      });

      clearForm();
    }
  
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
  padding: 8px 10px;
  border-radius: 5px;
  border: 2px solid #34495e;
  background-color: white;
  color: black;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

.tab-buttons button.active {
  background-color: #34495e;
  color: white;
}

.tab-buttons button:hover {
  background-color: darkgrey;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 5px;
  font-weight: bold;
  color: black;
}

input {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #2c3e50;
  background-color: white;
  color: white;
}

input::placeholder {
  color: #bdc3c7;
}

button {
  padding: 10px;
  background-color: black;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  transition: background-color 0.3s;
}

button:hover {
  background-color: darkgray;
}
  </style>
  