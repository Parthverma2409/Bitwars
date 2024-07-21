import express from 'express';
import { ChatOpenAI } from "@langchain/openai";
import { createOpenAIFunctionsAgent, AgentExecutor } from "langchain/agents";
import { pull } from "langchain/hub";

import { LangchainToolSet, ExecEnv } from "composio-core";

const app = express();
const PORT = process.env.PORT || 2001;

app.use(express.json());

(async () => {
    try {
        const body = "TITLE: HELLO WORLD, DESCRIPTION: HELLO WORLD for the repo - utkarsh-dixit/speedy"

        const llm = new ChatOpenAI({
            model: "gpt-4",
        });

        const toolset = new LangchainToolSet({
            apiKey: process.env.COMPOSIO_API_KEY,
            workspaceEnv: ExecEnv.DOCKER
        });

        const tools = await toolset.get_actions({
            actions: ["github_issues_create".toLowerCase()]
        });

        // await toolset.workspace.workspace.teardown();
        // const prompt = await pull(
        //     "hwchase17/openai-functions-agent"
        // );

        // const agent = await createOpenAIFunctionsAgent({
        //     llm,
        //     tools,
        //     prompt,
        // });

        // const agentExecutor = new AgentExecutor({
        //     agent,
        //     tools,
        //     verbose: true,
        // });

        // const result = await agentExecutor.invoke({
        //     input: "Please create another github issue with the summary and description with the following details of another issue:- , " + JSON.stringify(body)
        // });

    } catch (error) {
        console.error(error);
    }
})();