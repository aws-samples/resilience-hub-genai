import * as React from "react";
import Select from "@cloudscape-design/components/select";

interface Option {
  label: string;
  value: string;
}

interface PersonaSelectProps {
  onPersonaSelect: (persona: string) => void;
}

const PersonaSelect: React.FC<PersonaSelectProps> = ({ onPersonaSelect }) => {
  const [selectedOption, setSelectedOption] = React.useState<Option>({ label: "Choose a Persona", value: "0" });

  const handleChange = (option: Option) => {
    setSelectedOption(option);
    onPersonaSelect(option.value);
  };

  return (
    <Select
      selectedOption={selectedOption}
      onChange={({ detail }) => handleChange(detail.selectedOption as Option)}
      options={[
        { label: "Executive", value: "executive" },
        { label: "Manager", value: "manager" },
        { label: "Engineer", value: "engineer" }
      ]}
      placeholder="Choose a Persona"
    />
  );
};

export default PersonaSelect;
