// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import { Amplify } from 'aws-amplify';
import config from './cdk-output.json'



Amplify.configure({
    Auth: {
      Cognito: {
          userPoolId: config.AWSResilienceHubGenAI.COGNITOUSERPOOLID,
          userPoolClientId: config.AWSResilienceHubGenAI.COGNITOUSERPOOLCLIENTID,
          loginWith: {
            email: true,
          },
          passwordFormat: {
              minLength: 8,
              requireLowercase: true,
              requireUppercase: true,
              requireNumbers: true,
              requireSpecialCharacters: true,
          },
  
      },
    }
})

export const authConfig=Amplify.getConfig()
