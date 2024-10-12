// plugins/axios.js
import axios from 'axios';

export default defineNuxtPlugin((nuxtApp) => {
  const instance = axios.create({
    baseURL: 'http://127.0.0.1:8000', // Replace with your backend API URL
  });

  nuxtApp.provide('axios', instance);
});
