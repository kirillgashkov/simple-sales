import { defineStore } from "pinia";
import axios from "../api/axios";
import { User } from "../api/models";

export const useUsersStore = defineStore("users", {
  state: () => {
    return {
      user: null,
    }
  },
  actions: {
    async setUser(user) {
      this.user = user;
    },
    async loadUser() {
      await axios.get("/users/current")
        .then((response) => {
          this.setUser(new User(response.data));
        })
        .catch((error) => {
          const status_code = error.response && error.response.status;

          if (status_code === 401) {
            this.user = null;
          } else {
            console.error(error);
          }
        })
    },
    removeUser() {
      this.user = null;
    }
  },
})
