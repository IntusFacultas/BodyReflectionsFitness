<template>
  <div class="align-center">
    <page-title>Thank you for visiting!</page-title>
  </div>
</template>

<script>
import { PageTitle } from "@IntusFacultas/typography";
export const Logout = {
  components: { PageTitle },
  mounted() {
    let self = this;
    this.$store
      .dispatch("logout")
      .then(() => {
        self.$router.push({ name: "login" });
      })
      .catch(error => {
        if (error.response) {
          self.$store.commit("alert", {
            flavor: "Danger",
            title: "Logout failed.",
            content:
              "There was an issue logging you out. Please try refreshing the page in a few minutes.",
            buttons: [
              {
                text: "Ok",
                flavor: "Normal",
                action() {}
              }
            ]
          });
        } else {
          self.$store.commit("alert", {
            flavor: "Danger",
            title: "Logout failed.",
            content:
              "There was an issue contacting the server. Please try refreshing the page in a few minutes.",
            buttons: [
              {
                text: "Ok",
                flavor: "Normal",
                action() {}
              }
            ]
          });
        }
      });
  }
};
export default Logout;
</script>
