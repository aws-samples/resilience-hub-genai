// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import React from 'react';
//import ReactDOM from 'react-dom/client';
import ContentLayout from '@cloudscape-design/components/content-layout';
import Header from '@cloudscape-design/components/header';
import Link from '@cloudscape-design/components/link';
import HelpPanel from '@cloudscape-design/components/help-panel';
import TextContent from "@cloudscape-design/components/text-content";
import SidebarNav from '../../components/sidebar';
import Breadcrumbs from '../../components/breadcrumbs';
import Shell from '../../layouts/shell';
import { Authenticator } from '@aws-amplify/ui-react';
import { Amplify } from 'aws-amplify';
import { authConfig } from '../../config/auth';
import { loadConfig } from './loadconfig'
import '@aws-amplify/ui-react/styles.css';



Amplify.configure(authConfig);

function appLoaded() {
  const appLoaded = sessionStorage.getItem('appLoaded');
  if (!appLoaded) {
    loadConfig()
    sessionStorage.setItem('appLoaded', true.toString());
  }
}


export default function App() {
    appLoaded()
    return (
      <Authenticator hideSignUp>
        {({ signOut, user }) => (
          <Shell
              breadcrumbs={<Breadcrumbs active={{ text: 'Welcome', href: '/welcome/index.html' }} />}
              navigation={<SidebarNav />}
              tools={<HelpPanel header={<h2>Help panel</h2>} />}
            >
              <ContentLayout
                header={
                  <Header variant="h1" info={<Link variant="info">Info</Link>}>
                    Welcome
                  </Header>
                }
              >
                <TextContent>
                  <h2>Welcome to the AWS Resilience Hub GenAI Demo.</h2>
                  <p>By combining AWS Resilience Hub (ARH) and Amazon Bedrock, you can generate architectural findings in natural language to save time, better understand RTO/RPO requirements, and distribute assessments through a clear and concise view. ARH is a central location within the AWS Console to manage, define, and assess resilience goals with recommendations based on the AWS Well-Architected Framework. Amazon Bedrock is a fully managed service to build generative AI applications with foundation models (FMs) from leading AI companies such as Anthropic, Meta, Stability AI, Cohere, AI21 Labs, and Amazon all via a single API. Amazon Bedrock allows for integrating generative AI solutions within your application with the ability to test, fine-tune, and customize top FMs based on your use case.</p>
                </TextContent>
              </ContentLayout>
          </Shell>
        )}
      </Authenticator>
    );
  };
