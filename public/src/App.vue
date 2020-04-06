<template>
  <div id="app">
    <navbar
      :title="title"
      :left-items="leftItems"
      :right-items="rightItems"
      flavor="Primary"
    ></navbar>
    <theme-provider :theme="CUSTOM_THEME">
      <vue-toast
        class="toast-container"
        :parent-instance="this.$store"
      ></vue-toast>
      <vue-me :parent-instance="this.$store"></vue-me>
      <router-view></router-view>
    </theme-provider>
  </div>
</template>

<script>
import { ThemeProvider } from "vue-styled-components";
import VueMe from "@IntusFacultas/vue-me";
import VueToast from "@IntusFacultas/vue-toast";
import { Navbar } from "@IntusFacultas/navbar";
import { CUSTOM_THEME } from "./configuration";
export default {
  name: "App",
  components: {
    VueMe,
    ThemeProvider,
    Navbar,
    VueToast
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
            url: this.$router.resolve({ name: "dashboard" }).route.path
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
            url: this.$router.resolve({ name: "profile" }).route.path
          },
          {
            type: "item",
            html: `<i class="fa fa-sign-out" aria-hidden="true"></i>`, // rendered as HTML
            text: "Sign Out",
            url: this.$router.resolve({ name: "logout" }).route.path
          }
        ];
      } else {
        return [
          {
            type: "item",
            html: `<i class="fa fa-sign-in" aria-hidden="true"></i>`, // rendered as HTML
            text: "Sign In",
            url: this.$router.resolve({ name: "login" }).route.path
          }
        ];
      }
    }
  }
};
</script>

<style>
.toast-container {
  z-index: 2000;
  margin-top: 20px;
}
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
