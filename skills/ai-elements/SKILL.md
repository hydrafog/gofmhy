---
name: ai-elements
description: AI Elements is a component library and custom registry built on top of shadcn/ui to help you build AI-native applications faster.
---

# Introduction

What is AI Elements and why you should use it.

AI Elements is a component library and custom registry built on top of shadcn/ui to help you build AI-native applications faster. It provides pre-built components like conversations, messages and more.

Installing AI Elements is straightforward and can be done in a couple of ways. You can use the dedicated CLI command for the fastest setup, or integrate via the standard shadcn/ui CLI if you've already adopted shadcn's workflow.

`npx ai-elements@latest`

# Quick Start

Here are some basic examples of what you can achieve using components from AI Elements.

# Prerequisites

Before installing AI Elements, make sure your environment meets the following requirements:

- Node.js, version 18 or later
- A Next.js project with the AI SDK installed.
- shadcn/ui installed in your project. If you don't have it installed, running any install command will automatically install it for you.
- We also highly recommend using the AI Gateway and adding AI_GATEWAY_API_KEY to your env.local so you don't have to use an API key from every provider. AI Gateway also gives $5 in usage per month so you can experiment with models. You can obtain an API key here.

AI Elements is built targeting React 19 (no forwardRef usage) and Tailwind CSS 4.

# Installing Components

You can install AI Elements components using either the AI Elements CLI or the shadcn/ui CLI. Both achieve the same result: adding the selected component’s code and any needed dependencies to your project.

The CLI will download the component’s code and integrate it into your project’s directory (usually under your components folder). By default, AI Elements components are added to the `@/components/ai-elements/` directory (or whatever folder you’ve configured in your shadcn components settings).

After running the command, you should see a confirmation in your terminal that the files were added. You can then proceed to use the component in your code.

# Benefits

Why AI Elements is the best choice for building AI chat interfaces.

AI Elements provides a purpose-built component library for AI applications. Here's why you should use it.

## Fully Composable
Every component is designed as a building block. Compose Message, MessageContent, and MessageResponse together to create exactly the chat UI you need. No rigid structures or forced layouts.

```tsx
<Message from="assistant">
  <MessageContent>
    <MessageResponse>{text}</MessageResponse>
  </MessageContent>
</Message>
```

## More Than Just Styled Components
AI Elements integrates deeply with the AI SDK. Components understand streaming responses, handle loading states, and work seamlessly with hooks like useChat and useCompletion.

- Streaming support - Components like MessageResponse handle partial markdown gracefully
- Status awareness - UI adapts to pending, streaming, and complete states
- Type safety - Props align with AI SDK types like UIMessage

## Intuitive & Developer-Friendly
If you know React and TypeScript, you already know AI Elements. Components follow familiar patterns:
- Standard React props with TypeScript types
- Sensible defaults that work out of the box
- Full control when you need it

## Accessible & Themeable
Built on shadcn/ui, AI Elements inherits:
- WCAG 2.1 AA accessibility baseline
- CSS variables for easy theming
- Dark mode support built-in
- Semantic HTML throughout

Your existing shadcn/ui theme applies automatically.

## Fast, Flexible Installation
Install only what you need. The CLI adds components directly to your codebase:

`npx ai-elements@latest add message`

- No hidden dependencies
- Full source code access
- Modify components freely
- Tree-shaking friendly

# Setup

Get AI Elements installed and running in your project.

This guide walks you through setting up AI Elements in your project.

## Prerequisites
Before installing AI Elements, ensure your environment meets these requirements:
- Node.js 18 or later
- React 19
- Next.js 14+ (App Router recommended)
- AI SDK installed and configured
- shadcn/ui initialized in your project
- Tailwind CSS 4

If you don't have shadcn/ui installed, running any AI Elements install command will automatically set it up for you.

## AI Gateway (Recommended)
We recommend using AI Gateway for model access as it offers a single API key for multiple model providers, built-in fallback support, unified billing and more.

Add AI_GATEWAY_API_KEY to your .env.local file. Get your API key here.

## Installing Components
Use the AI Elements CLI to add components:

`npx ai-elements@latest add message`

Or use the shadcn CLI:

`npx shadcn@latest add @ai-elements/message`

Components are added to `@/components/ai-elements/` by default.

## Verify Installation
After installing a component, verify it works:
- Check that the component file exists in your components directory
- Import and use it in a page:

```tsx
import {
  Message,
  MessageContent,
  MessageResponse,
} from "@/components/ai-elements/message";

export default function Page() {
  return (
    <Message from="assistant">
      <MessageContent>
        <MessageResponse>Hello, world!</MessageResponse>
      </MessageContent>
    </Message>
  );
}
```

- Run your development server and confirm the component renders

# Usage

Learn how to use AI Elements components in your application.

Once an AI Elements component is installed, you can import it and use it in your application like any other React component. The components are added as part of your codebase (not hidden in a library), so the usage feels very natural.

## Example
After installing AI Elements components, you can use them in your application like any other React component. For example:

```tsx
"use client";

import {
  Message,
  MessageContent,
  MessageResponse,
} from "@/components/ai-elements/message";
import { useChat } from "@ai-sdk/react";

const Example = () => {
  const { messages } = useChat();

  return (
    <>
      {messages.map(({ role, parts }, index) => (
        <Message from={role} key={index}>
          <MessageContent>
            {parts.map((part, i) => {
              switch (part.type) {
                case "text":
                  return (
                    <MessageResponse key={`${role}-${i}`}>
                      {part.text}
                    </MessageResponse>
                  );
              }
            })}
          </MessageContent>
        </Message>
      ))}
    </>
  );
};

export default Example;
```

In the example above, we import the Message component from our AI Elements directory and include it in our JSX. Then, we compose the component with the MessageContent and MessageResponse subcomponents. You can style or configure the component just as you would if you wrote it yourself – since the code lives in your project, you can even open the component file to see how it works or make custom modifications.

## Extensibility
All AI Elements components take as many primitive attributes as possible. For example, the Message component extends HTMLAttributes<HTMLDivElement>, so you can pass any props that a div supports. This makes it easy to extend the component with your own styles or functionality.

## Customization
If you re-install AI Elements by rerunning npx ai-elements@latest, the CLI will ask before overwriting the file so you can save any custom changes you made.

After installation, no additional setup is needed. The component’s styles (Tailwind CSS classes) and scripts are already integrated. You can start interacting with the component in your app immediately.

For example, if you'd like to remove the rounding on Message, you can go to components/ai-elements/message.tsx and remove rounded-lg as follows:

```tsx
export const MessageContent = ({
  children,
  className,
  ...props
}: MessageContentProps) => (
  <div
    className={cn(
      "flex flex-col gap-2 text-sm text-foreground",
      "group-[.is-user]:bg-primary group-[.is-user]:text-primary-foreground group-[.is-user]:px-4 group-[.is-user]:py-3",
      className
    )}
    {...props}
  >
    <div className="is-user:dark">{children}</div>
  </div>
);
```

# Troubleshooting

What to do if you run into issues with AI Elements.

## Why are my components not styled?
Make sure your project is configured correctly for shadcn/ui in Tailwind 4 - this means having a globals.css file that imports Tailwind and includes the shadcn/ui base styles.

## I ran the AI Elements CLI but nothing was added to my project
Double-check that:
- Your current working directory is the root of your project (where package.json lives).
- Your components.json file (if using shadcn-style config) is set up correctly.
- You’re using the latest version of the AI Elements CLI: `npx ai-elements@latest`

## Theme switching doesn’t work — my app stays in light mode
Ensure your app is using the same data-theme system that shadcn/ui and AI Elements expect. The default implementation toggles a data-theme attribute on the `<html>` element. Make sure your tailwind.config.js is using class or data- selectors accordingly.

## The component imports fail with “module not found”
Check the file exists. If it does, make sure your tsconfig.json has a proper paths alias for `@/` i.e.
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

## My AI coding assistant can't access AI Elements components
- Verify your config file syntax is valid JSON.
- Check that the file path is correct for your AI tool.
- Restart your coding assistant after making changes.
- Ensure you have a stable internet connection.

# Philosophy

The principles that guide AI Elements design and development.

AI Elements is built on core principles that shape every component and decision.

## Composability
Components are building blocks, not black boxes. You combine small, focused pieces to create exactly what you need.

```tsx
<Message from="assistant">
  <MessageContent>
    <MessageResponse>{text}</MessageResponse>
  </MessageContent>
  <MessageActions>
    <MessageAction label="Copy" onClick={handleCopy}>
      <CopyIcon />
    </MessageAction>
  </MessageActions>
</Message>
```

This approach gives you:
- Flexibility - Add, remove, or rearrange pieces
- Control - Style and configure each part independently
- Clarity - Understand exactly what renders

## Simplicity
Do one thing well. Components have a clear purpose and minimal API surface. We avoid:
- Unnecessary props and options
- Complex configuration objects
- Hidden behavior

When in doubt, we leave it out. You can always extend components in your codebase.

## Accessibility
Every component follows accessibility best practices:
- Semantic HTML elements
- Proper ARIA attributes
- Keyboard navigation
- Screen reader support
- Sufficient color contrast

Accessibility isn't an afterthought—it's built into component architecture from the start.

## Performance
Components are optimized for real-world AI applications:
- Minimal re-renders during streaming
- Efficient DOM updates
- Tree-shakeable exports
- No runtime CSS-in-JS

## Developer Experience
Building AI interfaces should feel natural:
- Familiar patterns - Standard React props and hooks
- TypeScript first - Full type safety and autocomplete
- Good defaults - Works out of the box
- Full control - Customize when needed

## AI SDK Alignment
Components integrate deeply with the AI SDK:
- Props match AI SDK types
- Hooks work seamlessly
- Streaming behavior is handled correctly
- Status states are built-in

## shadcn/ui Foundation
AI Elements builds on shadcn/ui conventions:
- Components live in your codebase
- CSS variables for theming
- Tailwind CSS for styling
- Copy-paste friendly

Your existing shadcn/ui setup and theme apply automatically.
