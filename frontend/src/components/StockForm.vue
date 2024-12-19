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
      <div class="autocomplete-container" style="position: relative;">

        <label for="ticker">Stock Ticker</label>
        <input
          type="text"
          id="ticker"
          v-model="ticker"
          placeholder="e.g., AAPL"
          maxlength="5"
          autocomplete="off"
        />
        <ul v-if="suggestions.length" class="autocomplete-list">
          <li v-for="(suggestion, index) in suggestions" 
              :key="index" 
              @click="selectSuggestion(suggestion)">
            {{ suggestion }}
          </li>
        </ul>
      </div>
    </div>
    <div class="form-group">
      <label for="price">
        Price Per Share
      </label>
      <div class="input-container">
        <span class="dollar-sign">$</span>
        <input
          style="max-width : 145px;"
          type="number"
          id="price"
          v-model="price"
          placeholder="e.g., 150.00"
          autocomplete="off"
        />
      </div>
    </div>
    <div class="form-group">
      <label for="quantity">
        Number of Shares
      </label>
      <input
        type="number"
        id="quantity"
        v-model="quantity"
        placeholder="e.g., 10"
        min="1"
        autocomplete="off"
      />
    </div>
    <div class="form-group">
      <label for="date">Transaction Date</label>
      <input type="date" id="date" v-model="date" />
    </div>
    <div class="form-group">
      <label for="fees">Transaction Fees</label>
      <div class="input-container">
        <span class="dollar-sign">$</span>
        <input
          style="max-width : 145px;"
          type="number"
          id="fees"
          v-model="fees"
          placeholder="e.g., 10.00"
          autocomplete="off"
        />
      </div>    
    </div>
    <div class="form-checkbox" style="display: flex; justify-content: space-between;">
      <div>
        <label for="drip" style="margin-right: 0px;">Reinvest Dividends</label>
      </div>
      <div>
        <input
          type="checkbox"
          id="drip"
          v-model="drip"
        />
      </div>
    </div>
    <button @click="confirmStock">
      {{ isBuying ? 'Submit Buy Order' : 'Submit Sell Order' }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, defineEmits, watch } from "vue";
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const portfolioId = route.params.id; 

const emit = defineEmits(['update-data']);

const ticker = ref<string>("");
const price = ref<number | null>(null);
const quantity = ref<number | null>(null);
const date = ref<string>(new Date().toLocaleDateString("en-CA").split("T")[0]); // Default to current date
const fees = ref<number>(0)
const isBuying = ref(true); // Tracks whether the action is 'Buy' or 'Sell'
const drip = ref(false);

const apiUrl = import.meta.env.VITE_API_URL;

watch(ticker, (newValue) => {
  fetchSuggestions(newValue);
});

// Function to set the action type (Buy or Sell)
const setAction = (action: "buy" | "sell") => {
  isBuying.value = action === "buy";
};

const updateData = () => {
  emit('update-data'); // Emit the event
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
    fees: fees.value,
    drip: drip.value,
  };

  const isConfirmed = confirm(`
    Please confirm the following details:
    Action: ${stockDetails.action.toUpperCase()}
    Stock Ticker: ${stockDetails.ticker}
    Price Per Share: $${stockDetails.price.toFixed(2)}
    Quantity: ${stockDetails.quantity}
    Date: ${stockDetails.date}
    Transaction Fee: ${stockDetails.fees}
    Re-invest Dividends: ${stockDetails.drip}
  `);

  if (isConfirmed) {
    console.log("Stock transaction:", stockDetails);
    // Here, you would differentiate backend routes based on stockDetails.action
    // e.g., POST to `/stocks/buy` or `/stocks/sell`

    let url = `${apiUrl}/stocks/add/${portfolioId}`;

    if (stockDetails.action === 'sell'){
      url = `${apiUrl}/stocks/remove/${portfolioId}`;
    }

    axios.put(url, stockDetails)
    .then(response => {
      console.log('Response:', response.data);
    })
    .catch(error => {
        if (error.response) {
          // Server responded with a status outside the 2xx range
          console.error('Error status:', error.response.status);
          console.error('Error details:', error.response.data);
          
          // Show an alert to the user
          alert(`Error: ${error.response.data.detail || 'Something went wrong. Please try again later.'} Status Code: ${error.response.status}`);

        } else {
          console.error('Error:', error);
        }
      });

    clearForm();
    updateData();
  }
};

const clearForm = () => {
  ticker.value = "";
  price.value = null;
  quantity.value = null;
  date.value = new Date().toLocaleDateString("en-CA").split("T")[0];
};

const suggestions = ref<string[]>([]);

const fetchSuggestions = async (query: string) => {
  if (!query) {
    suggestions.value = [];
    return;
  }

  try {
    const response = await axios.get(`${apiUrl}/tickers`, { params: { q: query } });
    suggestions.value = response.data; // Assuming the API returns a list of ticker symbols
  } catch (error) {
    console.error("Error fetching suggestions:", error);
  }
};

const selectSuggestion = (suggestion: string) => {
  ticker.value = suggestion;
  suggestions.value = []; // Clear the suggestions
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
  color: black;
  max-width: 161px;
}

input::placeholder {
  color: #bdc3c7;
}

button {
  padding : 10px;
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

.input-container {
  display: flex;
  align-items: center;
  position: relative;
}

.dollar-sign {
  margin-right: 8px;
  font-size: 1rem;
  color: #666;
}

.autocomplete-container {
  position: relative; /* Keeps the list positioned relative to this container */
}

.autocomplete-list {
  position: absolute; /* This removes it from the normal flow */
  background-color: white;
  border: 1px solid #ccc;
  list-style: none;
  margin: 0;
  padding: 0;
  width: 100%; /* Adjust to fit container width */
  max-height: 150px;
  overflow-y: auto;
  z-index: 1000;
  top: 100%; /* Position it right below the input */
}

.autocomplete-list li {
  padding: 8px;
  cursor: pointer;
  color : black;
}

.autocomplete-list li:hover {
  background-color: #f0f0f0;
}
</style>
