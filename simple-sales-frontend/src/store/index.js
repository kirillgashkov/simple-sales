import { defineStore } from "pinia";

export const useStore = defineStore("main", {
  state: () => {
    return {
      user: null,
    }
  },
  actions: {
    setUser(user) {
      this.user = user;
    },
  },
})
