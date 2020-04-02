<template>
  <div class="relative-div">
    <sidebar
      class="custom-sidebar"
      flavor="BRF"
      sidebar-title="Profile"
      top-offset="0px"
      :items="sidebarItems"
      bottom-offset="0px"
    ></sidebar>
    <sidebar-offset-content>
      <router-view></router-view>
    </sidebar-offset-content>
  </div>
</template>

<script>
import { Sidebar, SidebarOffsetContent } from "@IntusFacultas/sidebar";
import SessionMixin from "../mixin";
export const Profile = {
  components: { Sidebar, SidebarOffsetContent },
  mixins: [SessionMixin],
  computed: {
    sidebarItems() {
      return [
        {
          type: "item",
          text: "Account Information & Security",
          icon: "",
          url: this.$router.resolve({ name: "profile-information" }).route.path,
          disabled: false,
          active: this.$route.path == "/profile/information"
        }
      ];
    }
  }
};
export default Profile;
</script>

<style>
.profile-view-container {
  padding: 15px 25px;
}
.custom-sidebar > div > span {
  padding-left: 7px;
}
.custom-sidebar li {
  text-align: center;
  margin-left: -7px;
}
</style>
