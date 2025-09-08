#!/usr/bin/env python3
"""
Demo script showing the multi-agent system in action.

This script demonstrates how different agents can be used for
specialized tasks while maintaining the main conversational flow.
"""

import asyncio
from forgebase.infrastructure.config import get_multi_agent_service


async def demo_multi_agent_system():
    """Demonstrate the multi-agent system capabilities."""
    print("🤖 Multi-Agent System Demo")
    print("=" * 50)

    # Initialize the multi-agent service
    service = get_multi_agent_service()

    # Show available agents
    print("\n📋 Available Agents:")
    agents = service.get_available_agents()
    for role, description in agents.items():
        print(f"  • {role}: {description}")

    print("\n" + "=" * 50)

    # Demo 1: Main conversational agent (PRD Facilitator)
    print("\n1️⃣ Main Agent Conversation:")
    print("-" * 30)

    user_message = "I want to create a new mobile app for task management"
    print(f"User: {user_message}")
    print("Agent: ", end="", flush=True)

    async for chunk in service.send_message_stream(user_message):
        print(chunk, end="", flush=True)
    print("\n")

    # Demo 2: Background technical analysis
    print("\n2️⃣ Technical Analysis (Background Agent):")
    print("-" * 40)

    requirements = (
        "Mobile app with real-time sync, offline support, and push notifications"
    )
    analysis = await service.analyze_technical_requirements(
        "demo-project-1", requirements
    )
    print(f"Requirements: {requirements}")
    print(f"Technical Analysis by {analysis['agent_role']}:")
    print(analysis["analysis"])
    print(f"Tools available: {', '.join(analysis['tools_used'])}")

    # Demo 3: Data collection
    print("\n3️⃣ Data Collection (Background Agent):")
    print("-" * 35)

    data = await service.collect_project_data("demo-project-1")
    print(f"Data collected by {data['agent_role']}:")
    print(data["collected_data"])
    print(f"Tools available: {', '.join(data['tools_used'])}")

    # Demo 4: Requirements validation
    print("\n4️⃣ Requirements Validation (Background Agent):")
    print("-" * 45)

    validation = await service.validate_requirements(requirements)
    print(f"Validation by {validation['agent_role']}:")
    print(validation["validation_result"])
    print(f"Tools available: {', '.join(validation['tools_used'])}")

    print("\n" + "=" * 50)
    print("✅ Demo completed!")
    print("\nKey Benefits:")
    print("  • Single user-facing agent for conversations")
    print("  • Specialized background agents for specific tasks")
    print("  • Tool-based architecture for data access")
    print("  • Simple configuration and extensibility")


if __name__ == "__main__":
    asyncio.run(demo_multi_agent_system())
