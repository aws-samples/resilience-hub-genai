// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0


export interface ModelOption{
    label: string;
    value: string;
}

export const modelList: ModelOption[] = [
    { label: 'Titan Text G1 - Premier', value: 'amazon.titan-text-premier-v1:0' },
    { label: 'Titan Text G1 - Lite', value: 'amazon.titan-text-lite-v1' },
    { label: 'Titan Text G1 - Express', value: 'amazon.titan-text-express-v1' },
    { label: 'Claude 3 Sonnet', value: 'anthropic.claude-3-sonnet-20240229-v1:0' },
    { label: 'Claude 3 Haiku', value: 'anthropic.claude-3-haiku-20240307-v1:0' },
    { label: 'Command R', value: 'cohere.command-r-v1:0' },
    { label: 'Command R+', value: 'cohere.command-r-plus-v1:0' },
    { label: 'Llama 3 8B Instruct', value: 'meta.llama3-8b-instruct-v1:0' },
    { label: 'Llama 3 70B Instruct', value: 'meta.llama3-70b-instruct-v1:0' },
    { label: 'Mistral 7B Instruct', value: 'mistral.mistral-7b-instruct-v0:2' },
    { label: 'Mixtral 8x7B Instruct', value: 'mistral.mixtral-8x7b-instruct-v0:1' },
    { label: 'Mistral Large', value: 'mistral.mistral-large-2402-v1:0' }
  ];
