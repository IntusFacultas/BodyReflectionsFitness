<template>
  <div class="align-center">
    <card :header="true" class="login-signup-card ">
      <template v-slot:header>
        <sub-section-title>Login</sub-section-title>
      </template>
      <template v-slot:body>
        <form>
          <vue-input
            :flavor="computeFlavor('username')"
            name="username"
            input-type="text"
            :required="true"
            label="Username"
            v-model="username"
            placeholder="Username"
          >
          </vue-input>
          <div class="form-error-message">
            <n-small
              :flavor="computeFlavor('usernameText')"
              v-for="(error, index) in errors.username"
              :key="`username-error-${index}`"
            >
              {{ error }}
            </n-small>
          </div>
          <vue-input
            :flavor="computeFlavor('password')"
            name="password"
            v-model="password"
            input-type="password"
            :required="true"
            label="Password"
            placeholder="Password"
          >
          </vue-input>
          <div class="form-error-message">
            <n-small
              :flavor="computeFlavor('passwordText')"
              v-for="(error, index) in errors.password"
              :key="`password-error-${index}`"
            >
              {{ error }}
            </n-small>
          </div>
          <div class="other-content">
            <div>
              <web-text>
                Not a member?
                <web-link :href="$router.resolve('register').route.path"
                  >Sign up!</web-link
                >
              </web-text>
            </div>
            <n-button
              role="button"
              flavor="Primary"
              @click="submit"
              :disabled="submitting"
            >
              <span>Submit </span>
              <i v-if="submitting" class="fa fa-spinner fa-pulse"></i>
            </n-button>
          </div>
        </form>
      </template>
    </card>
  </div>
</template>

<script>
import Card from "@IntusFacultas/card";
import {
  SubSectionTitle,
  WebLink,
  NSmall,
  WebText
} from "@IntusFacultas/typography";
import { VueInput } from "@IntusFacultas/input";
import { NButton } from "@IntusFacultas/button";
export const Login = {
  components: {
    Card,
    SubSectionTitle,
    VueInput,
    NButton,
    WebLink,
    NSmall,
    WebText
  },
  data() {
    return {
      username: "",
      password: "",
      submitting: false,
      errors: {
        username: [],
        password: []
      }
    };
  },
  mounted() {
    if (this.$route.meta.requiresAuth) {
      this.$store.dispatch("verifySession").then(this.validateSession);
    }
  },
  methods: {
    submit($e) {
      $e.preventDefault();
      let self = this;
      this.submitting = true;
      this.$store
        .dispatch("login", {
          username: this.username,
          password: this.password
        })
        .then()
        .catch(data => {
          if (data.response) {
            if (Array.isArray(data.response.data.username))
              self.errors.username = data.response.data.username;
            else self.errors.username = [];
            if (Array.isArray(data.response.data.password))
              self.errors.password = data.response.data.password;
            else self.errors.password = [];
            if (data.response.data.non_field_errors) {
              let content = "";
              for (let error of data.response.data.non_field_errors) {
                content += `<p class="alert-text">${error}</p>`;
              }
              self.$store.commit("alert", {
                flavor: "Danger",
                title: "Login failed.",
                content: content,
                buttons: [
                  {
                    text: "Ok",
                    flavor: "Normal",
                    action() {}
                  }
                ]
              });
            }
          } else {
            self.$store.commit("alert", {
              flavor: "Danger",
              title: "Login failed.",
              content: "There was an issue contacting the server.",
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
        .then(() => {
          self.submitting = false;
        });
    },
    computeFlavor(el) {
      if (el.indexOf("Text") != -1) {
        return "Danger";
      } else {
        if (el.indexOf("username") != -1) {
          if (this.errors.username.length > 0) {
            return "Danger";
          }
          return "LightBlue";
        } else {
          if (this.errors.password.length > 0) {
            return "Danger";
          }
          return "LightBlue";
        }
      }
    },
    validateSession() {
      this.$router.push({ name: "dashboard" });
    }
  }
};
export default Login;
</script>

<style>
.alert-text {
  font-family: "Open Sans Regular", -apple-system, BlinkMacSystemFont,
    "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji",
    "Segoe UI Emoji", "Segoe UI Symbol";
}
.align-center {
  display: flex;
  justify-content: center;
  align-items: center;
  align-content: center;
}
.login-signup-card {
  margin-top: 15%;
  width: 40%;
}
.other-content {
  margin-top: 25px;
  display: flex;
  justify-content: space-between;
}
.form-error-message {
  min-height: 17px;
  min-width: 1px;
}
</style>
