export const SessionMixin = {
  data() {
    return {
      stateVerified: false
    };
  },
  mounted() {
    if (this.$route.meta.requiresAuth) {
      this.$store
        .dispatch("verifySession")
        .catch(error => {
          if (error.response) {
            this.invalidateSession();
          } else {
            this.$store.commit("alert", {
              flavor: "Danger",
              title: "Network Issue",
              content: "There was an error contacting the server",
              buttons: [
                {
                  text: "Ok",
                  flavor: "Normal",
                  action() {
                    this.invalidateSession();
                  }
                }
              ]
            });
          }
        })
        .then(this.verifyState);
    } else if (this.$route.meta.guest) {
      this.$store
        .dispatch("verifySession")
        .then(this.validateSession)
        .catch(error => {
          if (!error.response) {
            this.$store.commit("alert", {
              flavor: "Danger",
              title: "Network Issue",
              content: "There was an error contacting the server",
              buttons: [
                {
                  text: "Ok",
                  flavor: "Normal",
                  action() {}
                }
              ]
            });
          }
        })
        .then(this.verifyState);
    }
  },
  methods: {
    verifyState() {
      this.stateVerified = true;
    },
    invalidateSession() {
      this.$router.push({ name: "login" });
    },
    validateSession() {
      this.$router.push({ name: "dashboard" });
    }
  }
};
export default SessionMixin;
