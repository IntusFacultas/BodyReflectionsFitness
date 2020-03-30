<template>
  <div v-if="stateVerified">
    DASHBOARD
  </div>
</template>

<script>
import SessionMixin from "../mixin";
export const Dashboard = {
  mixins: [SessionMixin]
};
export default Dashboard;
</script>
