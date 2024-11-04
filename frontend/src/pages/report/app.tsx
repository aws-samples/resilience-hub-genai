// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import React, { useState, useRef, useEffect } from 'react';

import ContentLayout from '@cloudscape-design/components/content-layout';
import Container from "@cloudscape-design/components/container";
import Header from "@cloudscape-design/components/header";
import SpaceBetween from "@cloudscape-design/components/space-between";
import Shell from '../../layouts/shell';
import HelpPanel from '@cloudscape-design/components/help-panel';
import Breadcrumbs from '../../components/breadcrumbs';
import SidebarNav from '../../components/sidebar';
import LoadingIndicator from '../../components/loadingIndicator';

import Button from "@cloudscape-design/components/button";

import PersonaSelect from '../../components/personaSelect';
import ApplicationSelect from '../../components/applicationSelect';

import { Authenticator, Divider } from '@aws-amplify/ui-react';
import { Amplify } from 'aws-amplify';
import Config from '../../config/cdk-output.json'
import { authConfig } from '../../config/auth';
import { fetchAuthSession } from 'aws-amplify/auth'
import '@aws-amplify/ui-react/styles.css';
import '../../layouts/shell/styles.css'




Amplify.configure(authConfig);


export default function App() {

  const apiGatewayUrl = Config.AWSResilienceHubGenAI.APIGATEWAYURL
  const generateReportEndpoint = apiGatewayUrl + Config.AWSResilienceHubGenAI.APIGATEWAYGENERATEREPORTPATH
  const [showReport, setShowReport] = useState(false);
  const [selectedApplication, setSelectedApplication] = useState('');
  const [selectedPersona, setSelectedPersona] = useState('');
  const [generatedReport, setGeneratedReport] = useState('');
  const [canGenerateReport, setCanGenerateReport] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const isFormComplete = () => {
    return selectedPersona !== '' && selectedApplication !== '';
  };


  useEffect(() => {
    setCanGenerateReport(isFormComplete());
  }, [selectedPersona, selectedApplication]);


  const handleGenerateReport = async () => {
    try {
      if (!showReport) {

        setIsLoading(true);
        const values = selectedApplication;
        const [app_arn, assessment_arn] = values.split('|');
        const { tokens } = await fetchAuthSession()
        const idToken = tokens?.idToken?.toString()
        const bearerToken = `Bearer ${idToken}`  


        const response = await fetch(generateReportEndpoint, {
          method: 'POST',
          headers: {
            'Authorization': bearerToken,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
            persona: selectedPersona,
            app_arn: app_arn,
            assessment_arn: assessment_arn }),
        });

        if (response.ok) {
          setShowReport(true);
          const responseData = await response.json();
          setGeneratedReport(responseData["generated-text"].replace(/\\n/g, "").slice(1, -1))
        } else {
          console.error('Error generating report:', response.status);
        }
        setIsLoading(false); 
      } else {
        setShowReport(false);
        setGeneratedReport('')
        setCanGenerateReport(false);
        setSelectedPersona('');
        setSelectedApplication(''); 
      }
    } catch (error) {
      console.error('Error generating report:', error);
      setIsLoading(false); 
    }
  };
  
  return (
    <Authenticator hideSignUp>
      {({ signOut, user }) => (
        <Shell
          breadcrumbs={<Breadcrumbs active={{ text: 'Report', href: '/report/index.html' }} />}
          navigation={<SidebarNav />}
          tools={<HelpPanel header={<h2>Help panel</h2>} />}
        >
          <ContentLayout>
          {!showReport ? (

              <Container
                header={
                  <Header
                    variant="h2"
                    description="Select the options below. Then press the Generate Report button."
                    actions={
                      <SpaceBetween
                        direction="horizontal"
                        size="xs"
                      >
                        <Button onClick={handleGenerateReport} disabled={!canGenerateReport}>
                          Generate Report
                        </Button>
                      </SpaceBetween>
                    }
                  >
                    Generate AWS Resilience Hub Report
                  </Header>
                }
              >
                <div className="spaced-components">
                  <h2>Persona</h2>
                  <PersonaSelect onPersonaSelect={(persona) => setSelectedPersona(persona)} />
                  <hr className="horizontal-line" />

                  <h2>Application</h2>
                  <ApplicationSelect onApplicationSelect={(value) => setSelectedApplication(value)} />
                  <hr className="horizontal-line" />
                  {isLoading && <LoadingIndicator />}
                </div>
              </Container>
            ) : (
              <Container
              header={
                <Header
                  variant="h2"
                  description={`Report for Persona ${selectedPersona}`} 
                  actions={
                    <SpaceBetween
                      direction="horizontal"
                      size="xs"
                    >
                      <Button onClick={handleGenerateReport}>Start Over</Button>
                    </SpaceBetween>
                  }
                >
                  Here is your Report
                </Header>
              }
            >
              <div dangerouslySetInnerHTML={{ __html: generatedReport }} />
            </Container>

            )}
          </ContentLayout>
        </Shell>
      )}
    </Authenticator>
  );
}