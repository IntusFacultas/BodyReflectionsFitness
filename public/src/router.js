import Vue from "vue";
import Router from "vue-router";
import Dashboard from "./views/Dashboard.vue";
import Login from "./views/Login";
import Logout from "./views/Logout";
import Signup from "./views/Signup";
import Profile from "./views/Profile";
import ProfileInformation from "./views/ProfileInformation";
import Exercises from "./views/Exercises";
import Overview from "./views/Overview";
// import store from "./store";
// import { HTTP, SERVER_CONFIGURATION } from "./configuration";
Vue.use(Router);

const routes = [
  {
    path: "/",
    redirect: { name: "dashboard" },
    meta: {
      requiresAuth: true
    }
  },
  {
    path: "/dashboard",
    name: "dashboard",
    redirect: "/dashboard/overview",
    component: Dashboard,
    meta: {
      requiresAuth: true
    },
    children: [
      {
        path: "overview",
        name: "dashboard-overview",
        component: Overview,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: "exercises",
        name: "dashboard-exercises",
        component: Exercises,
        meta: {
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: "/login",
    name: "login",
    component: Login,
    meta: {
      guest: true
    }
  },
  {
    path: "/logout",
    name: "logout",
    component: Logout,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: "/profile",
    name: "profile",
    redirect: "/profile/information",
    component: Profile,
    meta: {
      requiresAuth: true
    },
    children: [
      {
        path: "information",
        name: "profile-information",
        component: ProfileInformation,
        meta: {
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: "/register",
    name: "register",
    component: Signup,
    meta: {
      guest: true
    }
  }
  //   {
  //     path: "/system/:id",
  //     name: "system",
  //     component: SystemPage,
  //     props: true
  //   }
];
const router = new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: routes
});

router.onReady(function() {
  if (router.currentRoute.path === "/") {
    router.replace("/dashboard");
  }
});
// router.beforeEach((to, next) => {
//   if (to.matched.some(record => record.meta.requiresAuth)) {
//     HTTP.get(SERVER_CONFIGURATION.endpoints.verifySession())
//       .then(() => {
//         next();
//       })
//       .catch(() => {
//         next({
//           path: "/login",
//           params: { nextUrl: to.fullPath }
//         });
//       });
//   } else if (to.matched.some(record => record.meta.guest)) {
//     store
//       .dispatch("verifySession")
//       .then((data, to, next) => {
//         next({ name: "dashboard" });
//       })
//       .catch((data, to, next) => {
//         next();
//       });
//   }
// });

export default router;
