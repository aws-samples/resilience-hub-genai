import * as React from "react";
import Select from "@cloudscape-design/components/select";
import Config from '../../config/cdk-output.json'
import { fetchAuthSession } from 'aws-amplify/auth'


interface Option {
  label: string;
  value: string;
}

interface ApplicationSelectProps {
  onApplicationSelect: (value: string) => void;
}

const apiGatewayUrl = Config.AWSResilienceHubGenAI.APIGATEWAYURL
const getApplicationOptionsEndpoint = apiGatewayUrl + Config.AWSResilienceHubGenAI.APIGATEWAYGETAPPLICATIONSOPTIONSPATH

const ApplicationSelect: React.FC<ApplicationSelectProps> = ({ onApplicationSelect: onApplicationSelect }) => {
  const [selectedOption, setSelectedOption] = React.useState<Option>({ label: "Choose an Application", value: "0" });
  const [options, setOptions] = React.useState<Option[]>([]);
  

  React.useEffect(() => {
    const fetchData = async () => {

      const { tokens } = await fetchAuthSession()
      const idToken = tokens?.idToken?.toString()
      const bearerToken = `Bearer ${idToken}`

      try {
        const response = await fetch(getApplicationOptionsEndpoint, {
          method: 'GET',
          headers: {
            'Authorization': bearerToken,
            'Content-Type': 'application/json'
          }
        });

        const data = await response.json();
        const options = data.map((item: { app_name: string; app_arn: string, assessment_arn: string }) => ({
          label: item.app_name,
          value: `${item.app_arn}|${item.assessment_arn}`
        }));
        setOptions(options);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <Select
      selectedOption={selectedOption}
      onChange={({ detail }) => {
        const option = detail.selectedOption as Option;
        setSelectedOption(option);
        onApplicationSelect(option.value);
      }}
      options={options}
      placeholder="Choose an Application"
    />
  );
};

export default ApplicationSelect;