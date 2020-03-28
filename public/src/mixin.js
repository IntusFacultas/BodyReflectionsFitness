export const SessionMixin = {
  mounted() {
    if (this.$route.meta.requiresAuth) {
      this.$store.dispatch("verifySession").catch(this.invalidateSession);
    } else if (this.$route.meta.guest) {
      this.$store.dispatch("verifySession").then(this.validateSession);
    }
  },
  methods: {
    invalidateSession() {
      this.$router.push({ name: "login" });
    },
    validateSession() {
      this.$router.push({ name: "dashboard" });
    }
  }
};
export default SessionMixin;
