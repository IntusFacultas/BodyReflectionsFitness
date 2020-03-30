<template>
  <form>
    <div v-for="(field, index) in internalFields" :key="`field${index}`">
      <form-input
        v-if="field.type != 'select'"
        :label="field.label"
        :placeholder="field.placeholder"
        :name="field.name"
        :required="field.required"
        v-model="field.value"
        :errors="internalErrors[field.name]"
        :input-type="field.type"
        @input="validateField(field)"
        @keyup.enter="submitForm(index)"
      ></form-input>
      <raw-form-input
        :errors="internalErrors[field.name]"
        v-else-if="field.type == 'select'"
      >
        <n-label :for="field.name">{{ field.label }}</n-label>
        <select-me
          :name="field.name"
          :can-be-empty="!field.required"
          :options="field.options"
          v-model="field.value"
          @input="validateField(field)"
        ></select-me>
      </raw-form-input>
    </div>
    <div class="form-bottom-content" v-if="showBottom">
      <slot></slot>
      <div>
        <n-button
          type="button"
          flavor="Warning"
          @click="clearAll"
          :disabled="submitting"
          v-if="!disableClearing"
          class="form-button-spacing"
          >Clear</n-button
        >
        <n-button
          type="button"
          flavor="Primary"
          @click="submit($event)"
          :disabled="submitting || errorsExist || disableSubmission"
        >
          <span>Submit&nbsp;</span>
          <i v-if="submitting" class="fa fa-spinner fa-pulse"></i>
        </n-button>
      </div>
    </div>
  </form>
</template>
<script>
import FormInput from "./FormInput";
import RawFormInput from "./RawFormInput";
import SelectMe from "@IntusFacultas/select-me";
import { NButton } from "@IntusFacultas/button";
import { NLabel } from "@IntusFacultas/typography";
export const VueForm = {
  components: { FormInput, NButton, SelectMe, RawFormInput, NLabel },
  data() {
    return {
      internalFields: [],
      internalErrors: {}
    };
  },
  props: {
    showBottom: {
      type: Boolean,
      default: true
    },
    submitting: Boolean,
    disableSubmission: Boolean,
    disableClearing: Boolean,
    allowSubmissionOnEnter: {
      type: Boolean,
      default: true
    },
    fields: {
      type: Array,
      default() {
        return [];
      }
    },
    errors: {
      type: Object,
      default() {
        return {};
      }
    }
  },
  watch: {
    errors: {
      handler(newVal) {
        this.internalErrors = Object.assign({}, newVal);
      },
      deep: true
    }
  },
  mounted() {
    this.fields.forEach(field => {
      this.$watch(() => field, this.handleChange, { deep: true });
    });
    this.internalFields = this.fields.slice();
    for (let field of Object.keys(this.errors)) {
      this.internalErrors[field] = this.errors[field].slice();
    }
  },
  computed: {
    errorsExist() {
      for (let field of Object.keys(this.internalErrors)) {
        if (this.internalErrors[field].length != 0) {
          return true;
        }
      }
      return false;
    }
  },
  methods: {
    submitForm(index) {
      if (
        index == this.internalFields.length - 1 &&
        this.allowSubmissionOnEnter
      ) {
        this.$emit("submit");
      }
    },
    clearAll() {
      for (let field of this.internalFields) {
        field.value = "";
      }
      this.$emit("clear");
      this.$emit("fields", this.internalFields.slice());
    },
    objectDeepEquals(ob1, ob2) {
      let ob1Keys = Object.keys(ob1);
      let ob2Keys = Object.keys(ob2);
      if (ob1Keys.length !== ob2Keys.length) {
        return false;
      }
      for (let key of ob1Keys) {
        if (ob2Keys.indexOf(key) == -1) {
          return false;
        }
        if (typeof ob1[key] != typeof ob2[key]) {
          return false;
        }
        if (typeof ob1[key] == "object") {
          if (!this.objectDeepEquals(ob1[key], ob2[key])) {
            return false;
          }
        } else if (Array.isArray(ob1[key])) {
          if (!this.deepEquals(ob1[key], ob2[key])) {
            return false;
          }
        } else {
          if (ob1[key] != ob2[key]) {
            return false;
          }
        }
      }
      return true;
    },
    deepEquals(ar1, ar2) {
      let still_matches = true;
      let self = this;
      if (!Array.isArray(ar1) || !Array.isArray(ar2)) {
        return false;
      }
      if (ar1.length !== ar2.length) {
        return false;
      }
      ar1.forEach((val1, index) => {
        let val2 = ar2[index];
        if (val1 !== val2 && !self.objectDeepEquals(val1, val2)) {
          still_matches = false;
        }
      });
      return still_matches;
    },
    validateField(field) {
      if (typeof field.validation == "function") {
        let value = field.validation(field.value, this.internalFields);
        if (value) {
          if (this.internalErrors[field.name].indexOf(value) == -1) {
            this.internalErrors[field.name].push(value);
          }
          this.$emit("errors", this.internalErrors);
          return false;
        }
      }
      this.internalErrors[field.name] = [];
      this.$emit("fields", this.internalFields.slice());
      this.$emit("errors", this.internalErrors);
      return true;
    },
    handleChange() {
      this.internalFields = this.fields.slice();
    },
    submit($e) {
      $e.preventDefault();
      document.activeElement.blur();
      this.$emit("submit");
    }
  }
};
export default VueForm;
</script>

<style>
.form-button-spacing {
  margin-right: 5px;
}
</style>
