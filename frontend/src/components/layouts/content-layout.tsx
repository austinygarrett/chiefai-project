import * as React from 'react';

import './content-layout.scss';

type ContentLayoutProps = {
  children: React.ReactNode;
};

export const ContentLayout = ({ children }: ContentLayoutProps) => {
  return (
    <div>
      <div className="content-layout-content">{children}</div>
    </div>
  );
};
