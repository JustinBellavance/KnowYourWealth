<template>
  <div class="form">
    <div class="tab-buttons">
      <button
        :class="{ active: isBuying }"
        @click="setAction('buy')"
      >
        Buy
      </button>
      <button
        :class="{ active: !isBuying }"
        @click="setAction('sell')"
      >
        Sell
      </button>
    </div>

    <div class="form-group">
      <label for="ticker">Stock Ticker</label>
      <input
        type="text"
        id="ticker"
        v-model="ticker"
        placeholder="e.g., AAPL"
        maxlength="5"
      />
    </div>
    <div class="form-group">
      <label for="price">
        {{ isBuying ? 'Buy Price Per Share ($)' : 'Sell Price Per Share ($)' }}
      </label>
      <input
        type="number"
        id="price"
        v-model="price"
        placeholder="e.g., 150.00"
        step="0.01"
      />
    </div>
    <div class="form-group">
      <label for="quantity">
        {{ isBuying ? 'Number of Shares to Buy' : 'Number of Shares to Sell' }}
      </label>
      <input
        type="number"
        id="quantity"
        v-model="quantity"
        placeholder="e.g., 10"
        min="1"
      />
    </div>
    <div class="form-group">
      <label for="date">Transaction Date</label>
      <input type="date" id="date" v-model="date" />
    </div>
    <button @click="confirmStock">
      {{ isBuying ? 'Submit Buy Order' : 'Submit Sell Order' }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const ticker = ref<string>("");
const price = ref<number | null>(null);
const quantity = ref<number | null>(null);
const date = ref<string>(new Date().toISOString().split("T")[0]); // Default to current date
const isBuying = ref(true); // Tracks whether the action is 'Buy' or 'Sell'

// Function to set the action type (Buy or Sell)
const setAction = (action: "buy" | "sell") => {
  isBuying.value = action === "buy";
};

// Dummy submit function for backend integration
const confirmStock = () => {
  if (!ticker.value || !price.value || !quantity.value || !date.value) {
    alert("Please fill in all fields.");
    return;
  }

  const stockDetails = {
    action: isBuying.value ? "buy" : "sell",
    ticker: ticker.value.toUpperCase(),
    price: price.value,
    quantity: quantity.value,
    date: date.value,
  };

  const isConfirmed = confirm(`
    Please confirm the following details:
    Action: ${stockDetails.action.toUpperCase()}
    Stock Ticker: ${stockDetails.ticker}
    Price Per Share: $${stockDetails.price.toFixed(2)}
    Quantity: ${stockDetails.quantity}
    Date: ${stockDetails.date}
  `);

  if (isConfirmed) {
    console.log("Stock transaction:", stockDetails);
    // Here, you would differentiate backend routes based on stockDetails.action
    // e.g., POST to `/stocks/buy` or `/stocks/sell`
    clearForm();
  }
};

const clearForm = () => {
  ticker.value = "";
  price.value = null;
  quantity.value = null;
  date.value = new Date().toISOString().split("T")[0];
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
