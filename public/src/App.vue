<template>
  <div id="app">
    <navbar :title="title" :left-items="leftItems" :right-items="rightItems"></navbar>
    <theme-provider :theme="CUSTOM_THEME">
      <vue-me :parent-instance="this.$store"></vue-me>
      <router-view></router-view>
    </theme-provider>
  </div>
</template>

<script>
import { ThemeProvider } from "vue-styled-components";
import VueMe from "@IntusFacultas/vue-me";
import { Navbar } from "@IntusFacultas/navbar";
import { CUSTOM_THEME } from "./configuration";
export default {
  name: "App",
  components: {
    VueMe,
    ThemeProvider,
    Navbar
  },
  data() {
    return {
      CUSTOM_THEME,
      title: {
        text: "Body Reflections",
        url: "/",
        html: ""
      }
    };
  },
  computed: {
    leftItems() {
      if (this.$route.meta.requiresAuth) {
        return [
          {
            type: "item",
            html: "<i class='fa fa-home'  aria-hidden='true'></i>",
            text: "Home",
            url: this.$router.resolve("dashboard").route.path
          }
        ];
      } else {
        return [];
      }
    },
    rightItems() {
      if (this.$route.meta.requiresAuth) {
        return [
          {
            type: "item",
            html: `<i class="fa fa-user" aria-hidden="true"></i>`, // rendered as HTML
            text: "Profile",
            url: this.$router.resolve("profile").route.path
          },
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
[v-cloak] {
  display: none;
}
</style>
