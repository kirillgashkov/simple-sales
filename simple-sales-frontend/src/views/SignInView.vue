<script>
export default {
  data() {
    return {
      username: "",
      password: "",
    }
  },
  methods: {
    signIn() {
    },
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
