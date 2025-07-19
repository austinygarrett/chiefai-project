import Axios, { InternalAxiosRequestConfig } from 'axios';

import { env } from '@/config/env';
import { paths } from '@/config/paths';

function authRequestInterceptor(config: InternalAxiosRequestConfig) {
  if (config.headers) {
    config.headers.Accept = 'application/json';
  }

  config.withCredentials = true;
  return config;
}

export const api = Axios.create({
  baseURL: env.API_URL,
});

api.interceptors.request.use(authRequestInterceptor);
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    const message = error.response?.data?.message || error.message;
    //display notification

    if (error.response?.status === 401) {
      const searchParams = new URLSearchParams();
      const redirectTo =
        searchParams.get('redirectTo') || window.location.pathname;
      const isApp = window.location.pathname.includes('/app');

      if (isApp) {
        window.location.href = paths.auth.login.getHref();
      }
      console.log(
        `Forbidden access to ${redirectTo}. Redirecting to login page.`,
      );
      return Promise.resolve(error);
    }

    return Promise.reject(error);
  },
);
