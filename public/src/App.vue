<template>
  <div id="app">
    <theme-provider>
      <vue-me :parent-instance="this.$store"></vue-me>
      <router-view></router-view>
    </theme-provider>
  </div>
</template>

<script>
import { ThemeProvider } from "vue-styled-components";
import VueMe from "@IntusFacultas/vue-me";
export default {
  name: "App",
  components: {
    VueMe,
    ThemeProvider
  }
};
</script>

<style></style>
