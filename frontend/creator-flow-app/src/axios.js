import axios from "axios";
import getCookie from "./auth";

axios.defaults.baseURL = 'http://127.0.0.1:8000'

axios.interceptors.request.use(
    (config) => {
        const token = getCookie('access_token');
        if (token) {
            config.headers.Authorization = 'Bearer ${token}';
        }
        return config;
    },
    (error) => Promise.reject(error)
);

export default axios;