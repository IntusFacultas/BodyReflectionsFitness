<template>
  <div>
    DASHBOARD
  </div>
</template>

<script>
export const Dashboard = {
  mounted() {
    if (this.$route.meta.requiresAuth) {
      this.$store.dispatch("verifySession").catch(this.validateSession);
    }
  },
  methods: {
    validateSession() {
      this.$router.push({ name: "login" });
    }
  }
};
export default Dashboard;
</script>
