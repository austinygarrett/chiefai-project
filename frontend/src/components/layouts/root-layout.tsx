import { Stack } from '@mantine/core';
import { TopBar } from '../ui/topbar/topbar';

import './root-layout.scss';
export function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="container">
      <div className="content-container">
        <Stack gap={0} w={'100%'} className="main-content">
          <TopBar />
          <main>{children}</main>
        </Stack>
      </div>
    </div>
  );
}
