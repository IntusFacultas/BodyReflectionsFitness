<template>
  <div class="align-center">
    <card :header="true" class="login-signup-card ">
      <template v-slot:header>
        <sub-section-title>Create an Account</sub-section-title>
      </template>
      <template v-slot:body>
        <form>
          <category-title>Account Information</category-title>
          <form-input
            label="Username"
            placeholder="Username"
            name="username"
            :required="true"
            v-model="data.username"
            :errors="errors.username"
            input-type="text"
          ></form-input>
          <form-input
            label="Password"
            placeholder="Password"
            name="password"
            :required="true"
            v-model="data.password"
            :errors="errors.password"
            input-type="password"
          ></form-input>
          <form-input
            label="Confirm Password"
            placeholder="Passwords must match"
            name="confirmPassword"
            :required="true"
            v-model="data.confirmPassword"
            :errors="
              data.password == data.confirmPassword
                ? []
                : ['Passwords must match']
            "
            input-type="password"
          ></form-input>
          <div class="form-bottom-content">
            <div>
              <web-text>
                Already have an account?
                <web-link :href="$router.resolve('login').route.path"
                  >Log in.</web-link
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
  CategoryTitle,
  WebLink,
  WebText
} from "@IntusFacultas/typography";
import { NButton } from "@IntusFacultas/button";
import FormInput from "../components/FormInput";
import SessionMixin from "../mixin";
export const Signup = {
  mixins: [SessionMixin],
  data() {
    return {
      submitting: false,
      data: {
        username: "",
        password: "",
        confirmPassword: ""
      },
      errors: {
        username: [],
        password: []
      }
    };
  },
  components: {
    Card,
    FormInput,
    SubSectionTitle,
    CategoryTitle,
    WebLink,
    WebText,
    NButton
  },
  computed: {
    errorsExist() {
      for (let field of Object.keys(this.errors)) {
        if (this.errors[field].length != 0) {
          return true;
        }
      }
      return false;
    }
  },
  methods: {
    submit() {}
  }
};
export default Signup;
</script>
