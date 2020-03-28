<template>
  <div class="align-center">
    <card :header="true" class="login-signup-card ">
      <template v-slot:header>
        <sub-section-title>Login</sub-section-title>
      </template>
      <template v-slot:body>
        <vue-form
          :fields="fields"
          :errors="errors"
          :submitting="submitting"
          @fields="fields = $event"
          @submit="submit"
        >
          <web-text>
            Not a member?
            <web-link :href="$router.resolve('register').route.path"
              >Sign up!</web-link
            >
          </web-text>
        </vue-form>
      </template>
    </card>
  </div>
</template>

<script>
import Card from "@IntusFacultas/card";
import VueForm from "../components/Form";
import { SubSectionTitle, WebLink, WebText } from "@IntusFacultas/typography";
import { NButton } from "@IntusFacultas/button";
import SessionMixin from "../mixin";
export const Login = {
  mixins: [SessionMixin],
  components: {
    Card,
    SubSectionTitle,
    VueForm,
    NButton,
    WebLink,
    WebText
  },
  data() {
    return {
      fields: [
        {
          name: "username",
          label: "Username",
          type: "text",
          placeholder: "Username",
          value: "",
          required: true
        },
        {
          name: "password",
          label: "Password",
          type: "password",
          placeholder: "Password",
          value: "",
          required: true
        }
      ],
      submitting: false,
      errors: {
        username: [],
        password: []
      }
    };
  },
  methods: {
    submit() {
      let self = this;
      this.submitting = true;
      this.$store
        .dispatch("login", {
          username: this.fields[0].value,
          password: this.fields[1].value
        })
        .then(() => {
          this.$router.push({ name: "dashboard" });
        })
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
  min-width: 400px;
  margin-bottom: 100px;
}
.form-bottom-content {
  margin-top: 25px;
  display: flex;
  justify-content: space-between;
}
.form-error-message {
  min-height: 17px;
  min-width: 1px;
}
</style>
