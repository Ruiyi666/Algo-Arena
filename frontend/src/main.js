import './assets/tailwind.css'

import { createApp } from 'vue'

/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core';

/* import font awesome icon component */
// import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

/* import specific icons */
import {
    faCircle, faArrowUp, faGamepad, faHome, faQuestion, faBars, faTrophy, faBell,
    faEnvelope, faSun, faMoon, faUser
} from '@fortawesome/free-solid-svg-icons';
library.add(
    faCircle, faArrowUp, faGamepad, faHome, faQuestion, faBars, faTrophy, faBell,
    faEnvelope, faSun, faMoon, faUser
);


import { } from '@fortawesome/fontawesome-free';
import App from './App.vue';
import router from './router';
import store from './store';

const app = createApp(App);

app.use(router);
app.use(store);
app.mount('#app');
