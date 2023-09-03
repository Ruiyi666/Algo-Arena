// src/store/index.js

import { createStore } from 'vuex';

const store = createStore({
  state() {
    return {
      isLoggedIn: !!localStorage.getItem('token')
    };
  },
  mutations: {
    login(state, token) {
      state.isLoggedIn = true;
      localStorage.setItem('token', token);
    },
    logout(state) {
      state.isLoggedIn = false;
      localStorage.removeItem('token');
    }
  }
});

export default store;
