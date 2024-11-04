// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import React from 'react';
import AppLayout, { AppLayoutProps } from '@cloudscape-design/components/app-layout';
import TopNavigation from '@cloudscape-design/components/top-navigation';
import './styles.css';
import { Amplify } from 'aws-amplify';
import { signOut } from 'aws-amplify/auth';
import { authConfig } from '../../config/auth';

Amplify.configure(authConfig);

async function handleSignOut() {
  await signOut()
}

export interface ShellProps {
  breadcrumbs?: AppLayoutProps['breadcrumbs'];
  contentType?: Extract<AppLayoutProps.ContentType, 'default' | 'table' | 'form'>;
  tools?: AppLayoutProps['tools'];
  children?: AppLayoutProps['content'];
  navigation?: AppLayoutProps['navigation'];
  notifications?: AppLayoutProps['notifications'];
}

export default function Shell({ children, contentType, breadcrumbs, tools, navigation, notifications }: ShellProps) {

  return (
    <>
      <div id="top-nav">
        <TopNavigation
          identity={{
            title: 'AWS Resilience Hub GenAI Demo',
            href: '/welcome/index.html',
          }}
          i18nStrings={{
            overflowMenuTriggerText: 'More',
            overflowMenuTitleText: 'All',
          }}
          utilities={[
            {
              type: 'menu-dropdown',
              text: 'Links',
              items: [
                {
                  id: 'awsresiliencelink',
                  text: 'AWS Resilience',
                  href: 'https://aws.amazon.com/resilience/',
                  external: true,
                  externalIconAriaLabel: 'Opens the AWS Cloud Resilience site in a new tab.'
                },
                {
                  id: 'resiliencehublink',
                  text: 'Resilience Hub',
                  href: 'https://us-east-1.console.aws.amazon.com/resiliencehub/home?region=us-east-1',
                  external: true,
                  externalIconAriaLabel: 'Opens AWS Resilience Hub in a new tab.'
                }
              ]
            },
            {
              type: "button",
              text: "Sign Out",
              onClick: handleSignOut
            }
          ]}
        />
      </div>
      <AppLayout
        contentType={contentType}
        navigation={navigation}
        breadcrumbs={breadcrumbs}
        notifications={notifications}
        stickyNotifications={true}
        content={children}
        toolsHide={true}
        headerSelector="#top-nav"
        ariaLabels={{
          navigation: 'Navigation drawer',
          navigationClose: 'Close navigation drawer',
          navigationToggle: 'Open navigation drawer',
          notifications: 'Notifications',
        }}
      />
    </>
  );
}