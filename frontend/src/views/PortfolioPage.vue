<template>
    <div class="portfolio-page">
      <div class="sidebar">
        <StockSidebar />
      </div>
  
      <main class="content">
        <header class="page-header">
          <p class="text-6xl font-bold text-black">$50,000</p>
        </header>

        <section class="worth-graph">
            <WorthGraph :data="dummyData" :width=1300 :height=500></WorthGraph>
        </section>
  
        <section class="portfolio-overview">
          <h2>Overview</h2>
          <div class="overview-grid">
            <div class="card" v-for="(item, index) in overviewData" :key="index">
              <h3>{{ item.title }}</h3>
              <p>{{ item.value }}</p>
            </div>
          </div>
        </section>
  
        <section class="recent-transactions">
          <h2>Recent Transactions</h2>
          <ul>
            <li v-for="(transaction, index) in recentTransactions" :key="index">
              <strong>{{ transaction.type }}:</strong> {{ transaction.details }} - {{ transaction.date }}
            </li>
          </ul>
        </section>
      </main>
    </div>
  </template>
  
  <script setup lang="ts">
  import StockSidebar from "@/components/StockSidebar.vue";
  import WorthGraph from "@/components/WorthGraph.vue"
  
  const overviewData = [
    { title: "Total Net Worth", value: "$50,000" },
    { title: "Stocks", value: "$30,000" },
    { title: "Cash", value: "$20,000" },
  ];
  
  const recentTransactions = [
    { type: "Stock Purchase", details: "Bought 10 shares of AAPL", date: "2024-11-28" },
    { type: "Cash Deposit", details: "Deposited $500", date: "2024-11-27" },
  ];


  const dummyData = [
  { date: "2024-01-01", value: 1000, type: "Stocks" },
  { date: "2024-01-02", value: 1200, type: "Stocks" },
  { date: "2024-01-01", value: 500, type: "Cash" },
  { date: "2024-01-02", value: 550, type: "Cash" },
  { date: "2024-01-01", value: 300, type: "Bonds" },
  { date: "2024-01-02", value: 400, type: "Bonds" },
];

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
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px;
  }
  
  .card {
    background-color: #ffffff;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    text-align: center;
  }
  
  .card h3 {
    margin-bottom: 10px;
    font-size: 1.5rem;
    color: #34495e;
  }
  
  .card p {
    font-size: 1.2rem;
    color: #2c3e50;
  }
  
  .recent-transactions ul {
    list-style: none;
    padding: 0;
  }
  
  .recent-transactions li {
    background-color: #ffffff;
    border-radius: 8px;
    margin-bottom: 10px;
    padding: 10px 20px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  }
  
  .recent-transactions strong {
    color: #34495e;
  }
  </style>
  