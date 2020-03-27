import axios from "axios";

let baseURL;

if (!process.env.NODE_ENV || process.env.NODE_ENV === "development") {
  baseURL = "http://localhost:8000";
} else {
  baseURL = "https://www.bodyreflectionsfitness.fitness/";
}
// axios.defaults.xsrfCookieName = "csrftoken";
// axios.defaults.xsrfHeaderName = "X-CSRFToken";
export const HTTP = axios.create({
  baseURL: baseURL
  // xsrfCookieName: "csrftoken",
  // xsrfHeaderName: "X-CSRFToken"
});
const DEVELOPMENT_SERVER_CONFIGURATION = {
  endpoints: {
    exercises() {
      return "http://localhost:8000/api/filters/";
    },
    items() {
      return "http://localhost:8000/api/items/";
    },
    login() {
      return "http://localhost:8000/api/";
    }
  }
};

const PRODUCTION_SERVER_CONFIGURATION = {
  endpoints: {
    exercises() {
      return document.querySelector(
        'input[name="server-settings-FILTERSENDPOINT"]'
      ).value;
    },
    items() {
      return document.querySelector(
        'input[name="server-settings-ITEMSENDPOINT"]'
      ).value;
    },
    item() {
      return document.querySelector('input[name="server-settings-login"]')
        .value;
    }
  }
};

export const SERVER_CONFIGURATION =
  process.env.NODE_ENV === "production"
    ? PRODUCTION_SERVER_CONFIGURATION
    : DEVELOPMENT_SERVER_CONFIGURATION;

export default SERVER_CONFIGURATION;
