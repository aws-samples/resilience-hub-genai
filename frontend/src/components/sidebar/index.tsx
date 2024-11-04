// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import React from 'react';
import SideNavigation, { SideNavigationProps } from '@cloudscape-design/components/side-navigation';

const items: SideNavigationProps['items'] = [
  { type: 'link', text: 'Welcome', href: '/welcome/index.html' },
  { type: 'link', text: 'Report', href: '/report/index.html' },
];

export default function SidebarNav() {
  return (
    <>
      <SideNavigation
        activeHref={location.pathname}
        header={{ href: '/welcome/index.html', text: 'Menu' }}
        items={items}
      />
    </>
  );
}
