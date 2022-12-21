<script>
import http from "../http"
import { useStore } from "../store"
import { User } from "../models"
import router from "../router"


class SignInError {
  constructor({ message, isFormError }) {
    this.message = message;
    this.isFormError = isFormError;
  }
}


export default {
  data() {
    return {
      username: "",
      password: "",
      error: null
    }
  },
  methods: {
    signIn() {
      this.error = null;

      if (this.username === "") {
        this.error = new SignInError({
          message: "Имя пользователя не может быть пустым",
          isFormError: true,
        });
        return;
      }

      if (this.password === "") {
        this.error = new SignInError({
          message: "Пароль не может быть пустым",
          isFormError: true,
        });
        return;
      }

      const sessions_url = "/sessions"
      const sessions_payload = {}
      const sessions_config = {
        // Authorization: Basic
        auth: {
          username: this.username,
          password: this.password,
        }
      }

      http.post(sessions_url, sessions_payload, sessions_config)
        .then((response) => {
          http.get("/users/current")
            .then((response) => {
              const store = useStore();
              store.setUser(new User(response.data));
              console.log(store.user);
              router.push({ name: "home" })
            })
            .catch((error) => {
              this.handleGetCurrentUserError(error);
            })
        })
        .catch((error) => {
          this.handleCreateSessionError(error);
        })
    },
    handleCreateSessionError(error) {
      const status_code = error.response && error.response.status;

      if (status_code === 401) {
        this.error = new SignInError({
          message: "Неверное имя пользователя или пароль",
          isFormError: true,
        });
      } else {
        console.error(error)
        this.error = new SignInError({
          message: "Неизвестная ошибка",
          isFormError: false,
        });
      }
    },
    handleGetCurrentUserError(error) {
      console.error(error);
      this.error = new SignInError({
        message: "Неизвестная ошибка",
        isFormError: false,
      });
    },
  },
  beforeRouteEnter(to, from, next) {
    const store = useStore();
    if (store.user) {
      next({ name: "home" });
      return;
    }
    next();
  },
}
</script>

<template>
  <main class="container">
    <section class="section">
      <div class="columns is-centered">
        <div class="column is-half">
          <h1 class="title has-text-centered">Вход</h1>

          <form class="box" @submit.prevent="signIn">
            <div class="field">
              <label class="label">Имя пользователя</label>
              <div class="control">
                <input class="input" type="text" placeholder="ivanov" v-model="username">
              </div>
            </div>
            <div class="field">
              <label class="label">Пароль</label>
              <div class="control">
                <input class="input" type="password" placeholder="********" v-model="password">
              </div>
            </div>
            <div class="field">
              <div class="control">
                <div class="has-text-danger" v-if="error">
                  {{ error.message }}
                </div>
              </div>
            </div>
            <div class="field">
              <div class="control">
                <button class="button is-primary is-fullwidth">
                  <strong>Войти</strong>
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </section>
  </main>
</template>
