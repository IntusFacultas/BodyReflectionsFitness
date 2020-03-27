import Vue from "vue";
import Router from "vue-router";
import Dashboard from "./views/Dashboard.vue";
Vue.use(Router);

const routes = [
  {
    path: "/dashboard",
    name: "dashboard",
    component: Dashboard
  }
  //   {
  //     path: "/system/:id",
  //     name: "system",
  //     component: SystemPage,
  //     props: true
  //   }
];
const router = new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: routes
});

router.onReady(function() {
  if (router.currentRoute.path === "/") router.replace("/dashboard");
});
export default router;
