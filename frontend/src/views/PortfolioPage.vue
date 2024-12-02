<template>
    <div class="portfolio-page">
      <div class="sidebar">
        <StockSidebar />
      </div>
      
      <main class="content m-3">
        <header class="page-header">
          <p class="text-6xl font-bold text-black">{{cadConvert(totalNetWorth)}}</p>
          <div class="tab-buttons">
            <TabButton
              v-for="tab in tabs"
              :key="tab.label"
              :label="tab.label"
              :isActive="activeTab === tab.label"
              @activate="setActiveTab"
            />
          </div>
        </header>

        <section class="worth-graph">
            <WorthGraph :data="currentData" :width=1300 :height=500></WorthGraph>
        </section>
  
        <section class="portfolio-overview p-1 m-3">
        <p class="text-3xl">Details</p>
        <div class="overview-grid mt-4 mx-0 px-0">
          <AssetCard v-for="(asset, index) in overviewData" :key="index" :asset="asset" />
        </div>
      </section>
  
        <!-- <section class="recent-transactions">
          <h2>Recent Transactions</h2>
          <ul>
            <li v-for="(transaction, index) in recentTransactions" :key="index">
              <strong>{{ transaction.type }}:</strong> {{ transaction.details }} - {{ transaction.date }}
            </li>
          </ul>
        </section> -->
      </main>
    </div>
  </template>
  
  <script setup lang="ts">
  import StockSidebar from "@/components/StockSidebar.vue";
  import WorthGraph from "@/components/WorthGraph.vue"
  import TabButton from "@/components/TabButton.vue"
  import AssetCard from "@/components/AssetCard.vue"

  import { ref, computed, onMounted } from 'vue';
  import { useRoute } from 'vue-router';
  import axios from 'axios';

  const route = useRoute();
  const portfolioId = route.params.id; // Access the `id` from the URL

  const apiUrl = import.meta.env.VITE_API_URL;

  // Define tabs
  const tabs = [
    { label: 'All' },
    { label: 'Stocks' },
    { label: 'Cash'},
  ];

  const cadConvert = (number : number) => {
    return Intl.NumberFormat('en-CA', {style: 'currency', currency: 'CAD',}).format(number)
  }

  // Active tab state
  const activeTab = ref(tabs[0].label); // Default to 'All'

  // Function to update the active tab
  const setActiveTab = (label: string) => {
    activeTab.value = label;
  };

  // Computed property for dynamic data
  const currentData = computed(() => {
    if (activeTab.value === "All"){
      return assets.value;
    } else if (activeTab.value === "Stocks"){
      return stocks.value;
    } else if (activeTab.value === "Cash"){
      return cash.value;
    }
  });
  
  // const recentTransactions = [
  //   { type: "Stock Purchase", details: "Bought 10 shares of AAPL", date: "2024-11-28" },
  //   { type: "Cash Deposit", details: "Deposited $500", date: "2024-11-27" },
  // ];

  const assets = ref([]);
  const stocks = ref([]);
  const cash = ref([]);

  // Fetch assets on component mount
  const fetchAssets = async () => {
    try {
      const response = await axios.get(`${apiUrl}/assets/${portfolioId}`);
      console.log("Response:", response.data);
      assets.value = response.data;
    } catch (error) {
      console.error("Error:", error);
    }
  };

  // Computed properties for totals
  const stocksTotal = computed(() =>
    stockDetails.value.reduce((sum, item) => sum + item.value, 0)
  );

  const cashTotal = computed(() =>
      cash.value.length > 0 ? cash.value[cash.value.length - 1].value : 0
  );
  
  const totalNetWorth = computed(() => stocksTotal.value + cashTotal.value);

  const stockDetails = computed(() => {
    // Group the stocks by their name
    const groupedByStockName: Record<string, any[]> = {};

    // Step 1: Group by stock name
    stocks.value.forEach((stock) => {
      if (!groupedByStockName[stock.name]) {
        groupedByStockName[stock.name] = [];
      }
      groupedByStockName[stock.name].push(stock);
    });

    // Step 2: For each stock, find the entry with the latest date
    const latestStockPerName = Object.keys(groupedByStockName).map((name) => {
      // Get all the stocks for this name and sort them by date
      const stocksForName = groupedByStockName[name];

      // Sort by date in descending order to get the latest date first
      stocksForName.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());

      // Return the stock with the most recent date

      console.log(stocksForName[0].quantity * stocksForName[0].price);
      console.log(stocksForName[0].quantity, stocksForName[0].price);

      return {
        name,
        value: stocksForName[0].quantity * stocksForName[0].price,
        quantity: stocksForName[0].quantity,
        price: stocksForName[0].price,
      };
    });

    return latestStockPerName;
  });


  // Overview data for rendering
  const overviewData = computed(() => [
    { title: "Stocks", value: stocksTotal.value, details : stockDetails.value},
    { title: "Cash", value: cashTotal.value },
  ]);

  // Fetch assets on component mount
  const fetchStocks = async () => {
    try {
      const response = await axios.get(`${apiUrl}/stocks/${portfolioId}`);
      console.log("Response:", response.data);
      stocks.value = response.data;
    } catch (error) {
      console.error("Error:", error);
    }
  };
  
    // Fetch assets on component mount
    const fetchCash = async () => {
    try {
      const response = await axios.get(`${apiUrl}/cash/${portfolioId}`);
      console.log("Response:", response.data);
      cash.value = response.data;
    } catch (error) {
      console.error("Error:", error);
    }
  };

  // Fetch data when the component is mounted
  onMounted(() => {
    fetchAssets();
    fetchStocks();
    fetchCash();
  });

  </script>
  
  <style scoped>

  .portfolio-page {
    display: flex;
  }
  
  .content {
    flex: 1;
    padding: 20px;
    background-color: #f8f9fa;
    min-height: 100vh;
  }
  
  .page-header {
    margin-bottom: 30px;
    text-align: center;
  }
  
  .portfolio-overview {
    margin-bottom: 30px;
  }
  
  .portfolio-overview .overview-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
      gap: 20px;  /* Ensure there's enough gap between the cards */
  }

  .tab-buttons {
    display: flex; 
    justify-content: flex-start; 
    gap: 10px; 
    padding: 10px; 
  }
  </style>
  