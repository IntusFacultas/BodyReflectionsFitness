<template>
  <div class="profile-view-container">
    <card :header="true" class="profile-view-card-separation">
      <template v-slot:header>
        <sub-section-title>Account Information</sub-section-title>
      </template>
      <template v-slot:body>
        <vue-form
          :disable-clearing="true"
          :fields="userFields"
          :errors="userErrors"
          @fields="userFields = $event"
        >
          <span>&nbsp;</span>
        </vue-form>
      </template>
    </card>
    <card :header="true">
      <template v-slot:header>
        <sub-section-title>Change Password</sub-section-title>
      </template>
      <template v-slot:body>
        <vue-form
          :fields="changePasswordFormFields"
          :errors="changePasswordFormErrors"
          @fields="changePasswordFormFields = $event"
          :submitting="submittingPassword"
          @submit="submitChangePassword"
        >
          <span>&nbsp;</span>
        </vue-form>
      </template>
    </card>
  </div>
</template>

<script>
import Card from "@IntusFacultas/card";
import VueForm from "../components/Form";
import { SubSectionTitle } from "@IntusFacultas/typography";
import SessionMixin from "../mixin";
import { GENDER_VALUE_TO_TEXT_LOOKUP } from "../configuration";
export const Profile = {
  components: { Card, VueForm, SubSectionTitle },
  data() {
    return {
      changePasswordFormFields: [
        {
          name: "old_password",
          label: "Current Password",
          type: "password",
          placeholder: "",
          value: "",
          required: true
        },
        {
          name: "new_password1",
          label: "New Password",
          type: "password",
          placeholder: "",
          value: "",
          required: true
        },
        {
          name: "new_password2",
          label: "Confirm Password",
          type: "password",
          placeholder: "Password must match exactly",
          value: "",
          validation(value, fields) {
            let passwordField = fields.filter(
              field => field.name == "new_password1"
            )[0];
            if (value != passwordField.value) {
              return "Passwords must match";
            }
          },
          required: true
        }
      ],
      submittingPassword: false,
      changePasswordFormErrors: {},
      userFields: [],
      userErrors: {}
    };
  },
  methods: {
    /**
     * Lifted and changed from https://stackoverflow.com/questions/196972/convert-string-to-title-case-with-javascript/6475125
     * with thanks.
     */
    toTitleCase(input) {
      let output = input
        .split("_")
        .map(letter => {
          let firstLetter = letter[0].toUpperCase(); // H , a , Y  => H , A , Y
          let restLetters = letter.substring(1).toLowerCase(); // Ow, Re, OU => ow, re, ou
          return firstLetter + restLetters; // conbine together
        })
        .join(" ");
      return output;
    },
    updateFields() {
      this.userFields = [];
      let disallowedFields = ["is_staff", "date_joined", "username"];
      let fields = Object.keys(this.user);
      fields = fields.filter(x => disallowedFields.indexOf(x) == -1);
      for (let field of fields) {
        this.userFields.push({
          name: field,
          label: this.toTitleCase(field),
          type:
            field == "age"
              ? "number"
              : field == "email"
              ? "email"
              : field == "gender"
              ? "select"
              : "text",
          placeholder: "",
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
          value:
            field == "gender"
              ? [
                  {
                    value: this.user[field],
                    text: GENDER_VALUE_TO_TEXT_LOOKUP[this.user[field]]
                  }
                ]
              : this.user[field],
          required: true
        });
      }
    },
    formatFields(fields) {
      let formattedFields = {};
      for (let field of fields) {
        formattedFields[field.name] = field.value;
      }
      return formattedFields;
    },
    submitChangePassword() {
      this.submittingPassword = true;
      let self = this;
      this.$store
        .dispatch(
          "changePassword",
          this.formatFields(this.changePasswordFormFields)
        )
        .then(() => {
          for (let field of self.changePasswordFormFields) {
            field.value = "";
          }
          self.$store.commit("alert", {
            flavor: "Success",
            title: "Password changed.",
            content: "Next time you log in, use your new password.",
            buttons: [
              {
                text: "Ok",
                flavor: "Normal",
                action() {}
              }
            ]
          });
        })
        .catch(data => {
          if (data.response && data.response.status != 500) {
            self.changePasswordFormErrors = self.formatErrors(
              data.response.data.errors
            );
            let nonFieldErrors =
              typeof self.changePasswordFormErrors.non_field_errors !=
              "undefined"
                ? self.changePasswordFormErrors.non_field_errors
                : [];
            self.$forceUpdate();
            if (nonFieldErrors.length != 0) {
              let content = "";
              for (let error of nonFieldErrors) {
                content += `<p class="alert-text">${error}</p>`;
              }
              self.$store.commit("alert", {
                flavor: "Danger",
                title: "Password change failed.",
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
              title: "Password change failed.",
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
          self.submittingPassword = false;
        });
    }
  },
  watch: {
    user: {
      handler() {
        this.updateFields();
      },
      deep: true
    }
  },
  mounted() {
    this.updateFields();
  },
  computed: {},
  mixins: [SessionMixin]
};
export default Profile;
</script>

<style>
.profile-view-container {
  padding: 15px 0px;
  margin-right: 15px;
}
.profile-view-card-separation {
  margin-bottom: 25px;
}
</style>
