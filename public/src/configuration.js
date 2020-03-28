import axios from "axios";

let baseURL;

if (!process.env.NODE_ENV || process.env.NODE_ENV === "development") {
  baseURL = "http://localhost:8000";
} else {
  baseURL = "https://www.bodyreflections.fitness";
}
export const HTTP = axios.create({
  baseURL: baseURL
});
export const SERVER_CONFIGURATION = {
  endpoints: {
    exercises() {
      return "/api/exercises/";
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
