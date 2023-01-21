import axios from 'axios'

const httpServicePlugin = {
    // eslint-disable-next-line no-unused-vars
    install(Vue, options) {

        Vue.prototype.$axios = axios
        Vue.prototype.$setupAxios = function () {
            this.$axios.defaults.baseURL = process.env.API_URL || "http://127.0.0.1:8000/"
            this.$axios.defaults.headers['Content-Type'] = 'application/json'
            // this.$axios.interceptors.request.use(req => {
            //     req.headers['Authorization'] = `Bearer ${accessToken}`
            //     return req;
            // });
            this.$axios.interceptors.request.use(config => {
                this.$Progress.start();
                return config;
            });
            this.$axios.interceptors.response.use(
                response => {
                    this.$Progress.finish();
                    return Promise.resolve(response);
                },
                error => {
                    this.$Progress.finish();
                    return Promise.reject(error);
                }
            );
        }
    }
};

export default httpServicePlugin;