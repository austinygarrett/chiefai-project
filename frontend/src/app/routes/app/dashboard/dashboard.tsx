import { useEffect } from 'react';
import './dashboard.scss';
import { ContentLayout } from '@/components/layouts';
import { DashboardComponent } from '@/features/dashboard/components/dashboard';

export const DashboardRoute = () => {
  useEffect(() => {}, []);
  return (
    <>
      <ContentLayout>
        <div className="dashboard-container">
          <DashboardComponent />
        </div>
      </ContentLayout>
    </>
  );
};

export const AppRootErrorBoundary = () => {
  return <div>Something went wrong!</div>;
};
