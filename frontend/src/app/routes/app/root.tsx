import { useEffect } from 'react';
import { Outlet } from 'react-router-dom';
import './root.scss';
import { RootLayout } from '@/components/layouts/root-layout';

export const AppRoot = () => {
  useEffect(() => {}, []);
  return (
    <>
      <RootLayout>
        <Outlet />
      </RootLayout>
    </>
  );
};

export const AppRootErrorBoundary = () => {
  return <div>Something went wrong!</div>;
};
