<template>
  <div v-if="stateVerified">
    <sidebar
      class="custom-sidebar"
      flavor="BRF"
      sidebar-title="Dashboard"
      top-offset="48px"
      :items="sidebarItems"
      bottom-offset="0px"
    ></sidebar>
    <sidebar-offset-content>
      <router-view></router-view>
    </sidebar-offset-content>
  </div>
</template>

<script>
import SessionMixin from "../mixin";
import { Sidebar, SidebarOffsetContent } from "@IntusFacultas/sidebar";
export const Dashboard = {
  components: { Sidebar, SidebarOffsetContent },
  mixins: [SessionMixin],
  data() {
    return {
      sidebarItems: [
        {
          type: "item",
          text: "Overview",
          icon: "",
          url: this.$router.resolve({ name: "dashboard-overview" }).route.path,
          disabled: false,
          active: this.$route.path == "/dashboard/overview"
        },
        {
          type: "item",
          text: "Exercises",
          icon: "",
          url: this.$router.resolve({ name: "dashboard-exercises" }).route.path,
          disabled: false,
          active: this.$route.path == "/dashboard/exercises"
        }
      ]
    };
  }
};
export default Dashboard;
</script>
