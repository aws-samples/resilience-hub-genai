import * as React from "react";
import LoadingBar from "@cloudscape-design/chat-components/loading-bar";
import Box from "@cloudscape-design/components/box";


const LoadingIndicator = () => {
  return (
    <div aria-live="polite">
      <Box
        margin={{ bottom: "xs", left: "l" }}
        color="text-body-secondary"
      >
        Please Wait
      </Box>
      <LoadingBar variant="gen-ai" />
    </div>
  );
}

export default LoadingIndicator;