import axios from "axios";

let baseURL;

export const CUSTOM_THEME = {
  BRF: {
    color: {
      color: "#222"
    },
    background: {
      color: "#fcfcfc",
      hover: "#f2f2f2",
      focus: "#f2f2f2"
    },
    border: {
      color: "#fcfcfc"
    }
  }
};
export const GENDER_VALUE_TO_TEXT_LOOKUP = {
  1: "Male",
  2: "Female",
  3: "Prefer not to state",
  4: "Non-binary/Other"
};
if (!process.env.NODE_ENV || process.env.NODE_ENV === "development") {
  baseURL = "http://localhost:8000";
} else {
  baseURL = "https://www.bodyreflections.fitness";
}
export const HTTP = axios.create({
  baseURL: baseURL,
  withCredentials: true
});
export const SERVER_CONFIGURATION = {
  endpoints: {
    exercises() {
      return "/api/exercises/";
    },
    changePassword() {
      return "/api/auth/change-password/";
    },
    verifySession() {
      return "/api/auth/verify-session/";
    },
    logout() {
      return "/api/auth/logout/";
    },
    login() {
      return "/api/auth/login/";
    },
    signup() {
      return "/api/auth/signup/";
    }
  }
};

export default SERVER_CONFIGURATION;
