export const paths = {
  home: {
    path: '/',
    getHref: () => '/',

    pwReset: {
      path: '/reset',
      getHref: () => `/reset`,
    },
  },

  auth: {
    login: {
      path: '/',
      getHref: (redirectTo?: string | null | undefined) =>
        `/${redirectTo ? `?redirectTo=${encodeURIComponent(redirectTo)}` : ''}`,
    },
  },

  app: {
    root: {
      path: '/app',
      getHref: () => '/app',
    },
    dashboard: {
      path: '/app/dashboard',
      getHref: () => '/app/dashboard',
    },
  },
} as const;
