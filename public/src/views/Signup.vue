<template>
  <div class="align-center" v-if="stateVerified">
    <card :header="true" class="signup-card">
      <template v-slot:header>
        <sub-section-title>Create an Account</sub-section-title>
      </template>
      <template v-slot:body>
        <category-title>Account Information</category-title>
        <vue-form
          :fields="accountFields"
          :submitting="submitting"
          :errors="accountErrors"
          :allow-submission-on-enter="false"
          @fields="accountFields = $event"
          @errors="checkAccountErrors($event)"
          :show-bottom="false"
        ></vue-form>
        <hr />
        <category-title>Profile Information</category-title>
        <vue-form
          :fields="profileFields"
          :submitting="submitting"
          :errors="profileErrors"
          :disable-submission="accountInternalErrorsExist"
          @fields="profileFields = $event"
          @submit="submit"
        >
          <web-text>
            Already have an account?
            <web-link :href="$router.resolve('login').route.path">Log in.</web-link>
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
          name: "password1",
          label: "Password",
          type: "password",
          placeholder: "Password",
          value: "",
          required: true
        },
        {
          name: "password2",
          label: "Confirm Password",
          type: "password",
          placeholder: "Passwords must match",
          value: "",
          validation(value, fields) {
            let passwordField = fields.filter(
              field => field.name == "password1"
            )[0];
            if (value != passwordField.value) {
              return "Passwords must match";
            }
          },
          required: true
        }
      ],
      accountInternalErrorsExist: false,
      profileFields: [
        {
          name: "first_name",
          label: "First Name",
          type: "text",
          placeholder: "First name",
          value: "",
          required: true
        },
        {
          name: "last_name",
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
        first_name: [],
        last_name: []
      },
      accountErrors: {
        username: [],
        password1: [],
        password2: []
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
  computed: {
    formattedAccountFields() {
      let obj = {};
      for (let field of this.accountFields) {
        obj[field.name] = field.value;
      }
      return obj;
    },
    formattedProfileFields() {
      let obj = {};
      for (let field of this.profileFields) {
        obj[field.name] =
          field.type == "select"
            ? field.value.map(x => x.value)[0]
            : field.value;
      }
      return obj;
    }
  },
  methods: {
    checkAccountErrors(errors) {
      this.accountInternalErrorsExist = false;
      for (let field of Object.keys(errors)) {
        if (errors[field].length > 0) {
          this.accountInternalErrorsExist = true;
          break;
        }
      }
    },
    submit() {
      this.submitting = true;
      let self = this;
      this.$store
        .dispatch("signup", {
          accountInformation: this.formattedAccountFields,
          profileInformation: this.formattedProfileFields
        })
        .then(() => {
          self.$store.commit("alert", {
            flavor: "Success",
            title: "Account Created.",
            content: "Please login with your new account.",
            buttons: [
              {
                text: "Ok",
                flavor: "Normal",
                action() {
                  self.$router.push({ name: "login" });
                }
              }
            ]
          });
        })
        .catch(data => {
          if (data.response) {
            self.accountErrors = self.formatErrors(
              data.response.data.accountErrors
            );
            let nonFieldAccountErrors =
              typeof self.accountErrors.non_field_errors != "undefined"
                ? self.accountErrors.non_field_errors
                : [];
            self.profileErrors = self.formatErrors(
              data.response.data.profileErrors
            );
            let nonProfileErrors =
              typeof self.profileErrors.non_field_errors != "undefined"
                ? self.profileErrors.non_field_errors
                : [];
            let nonFieldErrors = [
              ...nonFieldAccountErrors,
              ...nonProfileErrors
            ];
            self.$forceUpdate();
            if (nonFieldErrors.length != 0) {
              let content = "";
              for (let error of nonFieldErrors) {
                content += `<p class="alert-text">${error}</p>`;
              }
              self.$store.commit("alert", {
                flavor: "Danger",
                title: "Account creation failed.",
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
              title: "Account creation failed.",
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
        .then(function() {
          self.submitting = false;
        });
    }
  }
};
export default Signup;
</script>

<style>
.signup-card {
  margin-top: 15px;
  margin-bottom: 100px;
  width: 40%;
  min-width: 400px;
}
</style>
