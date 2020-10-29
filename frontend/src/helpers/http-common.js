import axios from "axios";
import store from "../store"


const instance = axios.create({
  baseURL: "http://localhost:8000/",
  headers: {
    "Content-type": "application/json",
  }
});


instance.interceptors.request.use(function (config) {
  const user = store.getters["auth/user"];
  if (user) {
    config.headers["X-user"] = user.id
    config.headers["X-token"] = user.token
  }
  return config;
}, function (error) {
  return Promise.reject(error);
});


export default instance