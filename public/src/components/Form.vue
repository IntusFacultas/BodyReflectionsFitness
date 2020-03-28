<template>
  <form>
    <form-input
      v-for="(field, index) in internalFields"
      :key="`field${index}`"
      :label="field.label"
      :placeholder="field.placeholder"
      :name="field.name"
      :required="field.required"
      v-model="field.value"
      :errors="errors[field.name]"
      :input-type="field.type"
      @input="validateField(field)"
    ></form-input>
    <div class="form-bottom-content">
      <slot></slot>
      <div>
        <n-button
          type="button"
          flavor="Warning"
          @click="clearAll"
          :disabled="submitting"
          class="form-button-spacing"
          >Clear</n-button
        >
        <n-button
          type="button"
          flavor="Primary"
          @click="submit($event)"
          :disabled="submitting || errorsExist"
        >
          <span>Submit </span>
          <i v-if="submitting" class="fa fa-spinner fa-pulse"></i>
        </n-button>
      </div>
    </div>
  </form>
</template>
<script>
import FormInput from "./FormInput";
import { NButton } from "@IntusFacultas/button";
export const VueForm = {
  components: { FormInput, NButton },
  data() {
    return {
      internalFields: [],
      internalErrors: {}
    };
  },
  props: {
    submitting: Boolean,
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
        for (let field in Object.keys(newVal)) {
          if (!this.deepEquals(newVal[field], this.internalErrors[field])) {
            this.internalErrors[field] = newVal[field].slice();
          }
        }
      },
      deep: true
    }
  },
  mounted() {
    this.fields.forEach(field => {
      this.$watch(() => field, this.handleChange, { deep: true });
    });
    this.internalFields = this.fields.slice();
    this.internalErrors = Object.assign({}, this.errors);
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
    clearAll() {
      for (let field of this.internalFields) {
        field.value = "";
      }
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
        let value = field.validation(field.value);
        if (value) {
          this.internalErrors[field.name].push(value);
          return false;
        }
      }
      this.$emit("fields", this.internalFields.slice());
      return true;
    },
    handleChange() {
      this.internalFields = this.fields.slice();
    },
    submit($e) {
      $e.preventDefault();
      console.log($e);
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
