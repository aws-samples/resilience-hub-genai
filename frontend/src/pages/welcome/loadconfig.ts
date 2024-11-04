// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

function loadModelSettings() {
    const defaultModel = { label: "Amazon Titan Premier", value: "amazon.titan-text-premier-v1:0" };
    const defaultMaxTokens = 500;
    const defaultTemperature = 0.5;
    const defaultTopP = 0.2;
    const defaultTopK = 50;

    const storedModel = sessionStorage.getItem('modelId');
    const storedMaxTokens = sessionStorage.getItem('modelMaxTokens');
    const storedTemperature = sessionStorage.getItem('modelTemperature');
    const storedTopP = sessionStorage.getItem('modelTopP');
    const storedTopK = sessionStorage.getItem('modelTopK');

    if (!storedModel) {
    sessionStorage.setItem('modelId', defaultModel.value);
    }
    if (!storedMaxTokens) {
    sessionStorage.setItem('modelMaxTokens', defaultMaxTokens.toString());
    }
    if (!storedTemperature) {
    sessionStorage.setItem('modelTemperature', defaultTemperature.toString());
    }
    if (!storedTopP) {
    sessionStorage.setItem('modelTopP', defaultTopP.toString());
    }
    if (!storedTopK) {
    sessionStorage.setItem('modelTopK', defaultTopK.toString());
    }
}

export function loadConfig() {
    loadModelSettings()
}
