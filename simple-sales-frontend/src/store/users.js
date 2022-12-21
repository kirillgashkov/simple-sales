import { defineStore } from "pinia";
import http from "../http";
import { User } from "../models";

export const useUsersStore = defineStore("users", {
  state: () => {
    return {
      user: null,
      didLoadUser: false,
    }
  },
  actions: {
    loadUser() {
      return http.get("/users/current")
        .then((response) => {
          this.user = new User(response.data);
        })
        .catch((error) => {
          const status_code = error.response && error.response.status;

          if (status_code === 401) {
            this.user = null;
          } else {
            console.error(error)
          }
        })
        .then(() => {
          this.didLoadUser = true;
        });
    },
    removeUser() {
      this.user = null;
    }
  },
})
