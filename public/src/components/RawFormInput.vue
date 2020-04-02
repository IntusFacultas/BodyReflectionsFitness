<template>
  <div class="relative-div">
    <slot></slot>
    <div class="form-error-message">
      <n-small
        :flavor="computeFlavor('fieldText')"
        v-for="(error, index) in errors"
        :key="`field-error-${index}`"
      >{{ error }}</n-small>
    </div>
  </div>
</template>
<script>
import { NSmall } from "@IntusFacultas/typography";
export const RawFormInput = {
  components: { NSmall },
  data() {
    return {
      internalValue: ""
    };
  },
  watch: {
    value(newVal) {
      if (newVal != this.internalValue) {
        this.internalValue = newVal;
      }
    }
  },
  mounted() {
    this.internalValue = this.value;
  },
  props: {
    errors: {
      type: Array,
      default() {
        return [];
      }
    }
  },
  methods: {
    computeFlavor() {
      if (this.errors.length > 0) {
        return "Danger";
      }
      return "LightBlue";
    }
  }
};
export default RawFormInput;
</script>

<style>
.form-error-message {
  min-height: 17px;
  min-width: 1px;
}
</style>
