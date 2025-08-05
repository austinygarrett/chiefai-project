import { MantineProvider } from '@mantine/core';
import * as React from 'react';
import { createRoot } from 'react-dom/client';

import './index.scss';
import '@mantine/core/styles.css';

import { App } from './app';

const root = document.getElementById('root');
if (!root) throw new Error('No root element found');
createRoot(root).render(
  <MantineProvider>
    <App />
  </MantineProvider>,
);
