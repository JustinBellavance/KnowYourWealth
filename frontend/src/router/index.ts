import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import LandingPage from "@/views/LandingPage.vue";
import SignupPage from "@/views/SignUpPage.vue";
import PortfolioPage from "@/views/PortfolioPage.vue"

const routes: RouteRecordRaw[] = [
  { path: "/", component: LandingPage },
  { path: "/signup", component: SignUpPage },
  { path: "/portfolio/:id", component: PortfolioPage}
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;