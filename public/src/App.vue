<template>
  <div id="app" class="relative-div">
    <navbar :title="title" :right-items="rightItems"></navbar>
    <theme-provider class="relative-div">
      <vue-me :parent-instance="this.$store"></vue-me>
      <router-view class="relative-div"></router-view>
    </theme-provider>
  </div>
</template>

<script>
import { ThemeProvider } from "vue-styled-components";
import VueMe from "@IntusFacultas/vue-me";
import { Navbar } from "@IntusFacultas/navbar";
export default {
  name: "App",
  components: {
    VueMe,
    ThemeProvider,
    Navbar
  },
  data() {
    return {
      title: {
        text: "Body Reflections",
        url: "/",
        html: ""
      }
    };
  },
  computed: {
    rightItems() {
      if (this.$route.meta.requiresAuth) {
        return [
          {
            type: "item",
            html: `<i class="fa fa-sign-out" aria-hidden="true"></i>`, // rendered as HTML
            text: "Sign Out",
            url: this.$router.resolve("logout").route.path
          }
        ];
      } else {
        return [
          {
            type: "item",
            html: `<i class="fa fa-sign-in" aria-hidden="true"></i>`, // rendered as HTML
            text: "Sign In",
            url: this.$router.resolve("login").route.path
          }
        ];
      }
    }
  }
};
</script>

<style>
.relative-div {
  position: relative;
}
body {
  margin: 0;
}
</style>
