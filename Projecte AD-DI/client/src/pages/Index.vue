<template>
  <q-page class="bg-light-blue window-height window-width row justify-center items-center">
    <div class="column">
      <div class="row">
        <h5 class="text-h5 text-white q-my-md">Login</h5>
      </div>
      <div class="row">
        <q-card square bordered class="q-pa-lg shadow-1">
          <q-card-section>
            <q-form class="q-gutter-md">
              <q-input square filled clearable v-model="nombre" type="text" label="Username" :rules="[val => !!val || 'Username is missing']"/>
              <q-input square filled clearable v-model="password" type="password" label="Password" :rules="[val => !!val || 'Password is missing']"/>
            </q-form>
          </q-card-section>
          <q-card-actions class="q-px-md">
            <q-btn unelevated color="light-blue-7" size="lg" class="full-width" label="LOGIN" @click="Login"/>
          </q-card-actions>
          <q-card-section class="text-center q-pa-none">
            <p class="text-grey-6"> No estàs registrat? <a href="http://localhost:8080/#/registro"> Registra't </a> </p>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>

import { api } from 'boot/axios'

export default {
  name: 'Login',
  data () {
    return {
      nombre: '',
      password: ''
    }
  },
  methods: {
    Login () {
      api.post('/api/login', {
        username: this.nombre,
        password: this.password
      })
        .then((response) => {
          if (response.data.ok) {
            this.$store.commit('setToken', response.data.accessToken)
            this.$store.commit('setUserInfo', this.nombre)
            this.$store.commit('setRefreshToken', response.data.refreshTokenSecret)
            this.$q.notify({
              message: 'Login Correcte',
              type: 'positive',
              position: 'center'
            })
            this.$router.replace('/inicio')
          } else {
            this.$q.notify({
              message: 'Login Incorrecte',
              type: 'warning',
              position: 'center'
            })
          }
        })
        .catch(function (error) {
          console.log(error)
        })
    }
  }
}
</script>
