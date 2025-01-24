<template>
    <HeaderHome></HeaderHome>
    <div class="portfolio-page">
      <div class="sidebar">
        <StockSidebar @update-data="refreshData"/>
      </div>
      
      <main ref='myDiv' class="content m-3">
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
          <div v-if="ninetyFivePercentWidth">
            <WorthGraph :data="graphData" :width="ninetyFivePercentWidth" :height="500"></WorthGraph>
          </div>
        </section>
  
        <section class="portfolio-overview p-1 m-3">
          <div class="overview-grid mt-4 mx-0 px-0">
            <StockCard v-for="(asset, index) in overviewStockData" :key="index" :asset="asset" />
          </div>
          <div class="overview-grid mt-4 mx-0 px-0">
            <AssetCard v-for="(asset, index) in overviewAssetData" :key="index" :asset="asset" />
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
  import StockCard from "@/components/StockCard.vue"

  import HeaderHome from "@/components/HeaderHome.vue"

  import { ref, computed, onMounted, onUpdated } from 'vue';
  import { useRoute } from 'vue-router';
  import axios from 'axios';
  import debounce from 'lodash/debounce';

  const route = useRoute();
  const portfolioId = route.params.id;

  const myDiv = ref(null);
  const ninetyFivePercentWidth = ref(0); // Default value for 95% width

  const updateWidth = () => {
    if (myDiv.value) {
      var divWidth = myDiv.value.offsetWidth; // Get the width of the <main> element
      ninetyFivePercentWidth.value = divWidth * 0.97; // Set the width to 95% of the div
    }
  };

  const optimizedUpdate = debounce(() => {
    updateWidth();
  }, 200); // Debouncing to avoid frequent calculations during resizing

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
  const graphData = computed(() => {
    if (activeTab.value === "All"){
      return assets.value;
    } else if (activeTab.value === "Stocks"){
      return stocks.value;
    } else if (activeTab.value === "Cash"){
      return cash.value;
    }
  });

  const refreshData = () => {
    fetchAssets();
    fetchStocks();
    fetchCash();
  };

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
    cashDetails.value.reduce((sum, item) => sum + item.value, 0)
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

      return {
        name,
        value: stocksForName[0].quantity * stocksForName[0].price,
        quantity: stocksForName[0].quantity,
        price: stocksForName[0].price,
      };
    });

    return latestStockPerName;
  });

  
  const cashDetails = computed(() => {
    // Group the cashs by their name
    const groupedByCashName: Record<string, any[]> = {};

    // Step 1: Group by cash name
    cash.value.forEach((cash) => {
      if (!groupedByCashName[cash.name]) {
        groupedByCashName[cash.name] = [];
      }
      groupedByCashName[cash.name].push(cash);
    });

    // Step 2: For each cash, find the entry with the latest date
    const latestCashPerName = Object.keys(groupedByCashName).map((name) => {
      // Get all the cashs for this name and sort them by date
      const cashForName = groupedByCashName[name];

      // Sort by date in descending order to get the latest date first
      cashForName.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());

      // Return the stock with the most recent date

      return {
        name,
        interest : cashForName[0].interest,
        value: cashForName[0].value
      };
    });

    return latestCashPerName;
  });


  // Overview data for rendering
  const overviewStockData = computed(() => [
    { title: "Stocks", value: stocksTotal.value, details : stockDetails.value},
  ])

  // this is for when we add more assets
  const overviewAssetData = computed(() => [
    { title: "Cash", value: cashTotal.value, details : cashDetails.value },
  ]);

  const fetchStocks = async () => {
    try {
      const response = await axios.get(`${apiUrl}/stocks/${portfolioId}`);
      stocks.value = response.data;
    } catch (error) {
      console.error("Error:", error);
    }
  };
  
    const fetchCash = async () => {
    try {
      const response = await axios.get(`${apiUrl}/cash/${portfolioId}`);
      cash.value = response.data;
    } catch (error) {
      console.error("Error:", error);
    }
  };

  // Fetch data when the component is mounted
  onMounted(() => {
    optimizedUpdate(); // Initial calculation on mount
    window.addEventListener('resize', optimizedUpdate); // Recalculate width on resize

    fetchAssets();
    fetchStocks();
    fetchCash();
  });

  // Clean up the event listener when the component is unmounted
  onUpdated(() => {
    optimizedUpdate(); // Recalculate on component updates (optional)
  });

  </script>
  
  <style scoped>

  .portfolio-page {
    display: flex;
  }
  
  .content {
    flex: 1;
    padding: 20px;
    background-color: white;
    min-height: 100vh;
  }
  
  .page-header {
    margin-bottom: 30px;
    text-align: center;
  }
  
  .portfolio-overview {
    margin-bottom: 30px;
    width: 96%;
  }

  .tab-buttons {
    display: flex; 
    justify-content: flex-start; 
    gap: 10px; 
    padding: 10px; 
  }
  </style>
  