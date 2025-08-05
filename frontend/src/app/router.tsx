import { QueryClient, useQueryClient } from '@tanstack/react-query';
import { useMemo } from 'react';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';

import { AppRoot, AppRootErrorBoundary } from './routes/app/root';

import { paths } from '@/config/paths';
import { ProtectedRoute } from '@/lib/auth';

export const createAppRouter = (queryClient: QueryClient) =>
  createBrowserRouter([
    {
      path: '/',
      children: [
        {
          path: paths.auth.login.path,
          lazy: async () => {
            const { LoginRoute } = await import('./routes/auth/login');
            return { Component: LoginRoute };
          },
        },
        {
          path: paths.app.root.path,
          element: (
            <ProtectedRoute>
              <AppRoot />
            </ProtectedRoute>
          ),
          ErrorBoundary: AppRootErrorBoundary,
          children: [
            {
              path: paths.app.dashboard.path,
              lazy: async () => {
                const { DashboardRoute } = await import(
                  './routes/app/dashboard/dashboard'
                );
                return {
                  Component: DashboardRoute,
                };
              },
              ErrorBoundary: AppRootErrorBoundary,
            },
          ],
        },
        {
          path: '*',
          lazy: async () => {
            const { NotFoundRoute } = await import('./routes/not-found');
            return {
              Component: NotFoundRoute,
            };
          },
          ErrorBoundary: AppRootErrorBoundary,
        },
      ],
    },
  ]);

export const AppRouter = () => {
  const queryClient = useQueryClient();

  const router = useMemo(() => createAppRouter(queryClient), [queryClient]);

  return <RouterProvider router={router} />;
};
