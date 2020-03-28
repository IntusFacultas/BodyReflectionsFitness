<template>
  <div class="align-center">
    <card :header="true" class="login-signup-card ">
      <template v-slot:header>
        <sub-section-title>Create an Account</sub-section-title>
      </template>
      <template v-slot:body>
        <category-title>Account Information</category-title>
        <vue-form
          :fields="accountFields"
          :submitting="submitting"
          :errors="accountErrors"
          :show-bottom="false"
        >
        </vue-form>
        <hr />
        <category-title>Profile Information</category-title>
        <vue-form
          :fields="profileFields"
          :submitting="submitting"
          :errors="profileErrors"
        >
          <web-text>
            Already have an account?
            <web-link :href="$router.resolve('login').route.path"
              >Log in.</web-link
            >
          </web-text>
        </vue-form>
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
import VueForm from "../components/Form";
import SessionMixin from "../mixin";
export const Signup = {
  mixins: [SessionMixin],
  data() {
    return {
      submitting: false,
      accountFields: [
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
          type: "text",
          placeholder: "password",
          value: "",
          required: true
        },
        {
          name: "passwordConfirm",
          label: "Confirm Password",
          type: "text",
          placeholder: "Passwords must match",
          value: "",
          validation(value, fields) {
            let passwordField = fields.filter(
              field => field.name == "password"
            )[0];
            if (value != passwordField.value) {
              return "Passwords must match";
            }
          },
          required: true
        }
      ],
      profileFields: [
        {
          name: "firstName",
          label: "First Name",
          type: "text",
          placeholder: "First name",
          value: "",
          required: true
        },
        {
          name: "lastName",
          label: "Last Name",
          type: "text",
          placeholder: "Last Name",
          value: "",
          required: true
        },
        {
          name: "age",
          label: "Age",
          type: "number",
          placeholder: "Age",
          value: "",
          required: true
        },
        {
          name: "gender",
          label: "Gender",
          type: "select",
          options: [
            {
              text: "Male",
              value: 1
            },
            {
              text: "Female",
              value: 2
            },
            {
              text: "Prefer not to state",
              value: 3
            },
            {
              text: "Non-binary/Other",
              value: 4
            }
          ],
          value: [],
          required: true
        },
        {
          name: "email",
          label: "Preferred Email",
          type: "text",
          placeholder: "Email",
          value: "",
          required: true
        }
      ],
      profileErrors: {
        email: [],
        age: [],
        gender: [],
        firstName: [],
        lastName: []
      },
      accountErrors: {
        username: [],
        password: [],
        confirmPassword: []
      }
    };
  },
  components: {
    Card,
    VueForm,
    SubSectionTitle,
    CategoryTitle,
    WebLink,
    WebText,
    NButton
  },
  computed: {},
  methods: {
    submit() {}
  }
};
export default Signup;
</script>
