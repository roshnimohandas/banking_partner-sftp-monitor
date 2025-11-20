"""
MCP Server for SFTP file monitoring with tools for:
- Connecting to SFTP servers
- Checking file existence
- Validating file metadata
- Sending alerts
"""
from typing import Any
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mcp.server import Server
from mcp.types import Tool, TextContent
import json
import logging
from datetime import datetime

# Import validators
from src.validators.sftp_client import SFTPClient
from src.validators.file_validator import FileValidator

# Import notification modules
try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
    SLACK_AVAILABLE = True
except ImportError:
    SLACK_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
app = Server("banking-sftp-monitor")

# Store active SFTP connections
active_connections = {}


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools"""
    return [
        Tool(
            name="connect_sftp",
            description="Connect to an SFTP server using credentials",
            inputSchema={
                "type": "object",
                "properties": {
                    "connection_name": {
                        "type": "string",
                        "description": "Name for this SFTP connection"
                    },
                    "host": {
                        "type": "string",
                        "description": "SFTP server hostname"
                    },
                    "port": {
                        "type": "integer",
                        "description": "SFTP server port (default: 22)",
                        "default": 22
                    },
                    "username": {
                        "type": "string",
                        "description": "Username for authentication"
                    },
                    "password": {
                        "type": "string",
                        "description": "Password for authentication (optional if using key)"
                    },
                    "private_key_path": {
                        "type": "string",
                        "description": "Path to private key file (optional if using password)"
                    }
                },
                "required": ["connection_name", "host", "username"]
            }
        ),
        Tool(
            name="list_files",
            description="List files in a directory on SFTP server",
            inputSchema={
                "type": "object",
                "properties": {
                    "connection_name": {
                        "type": "string",
                        "description": "Name of the SFTP connection"
                    },
                    "remote_path": {
                        "type": "string",
                        "description": "Remote directory path (default: current directory)",
                        "default": "."
                    }
                },
                "required": ["connection_name"]
            }
        ),
        Tool(
            name="check_file_exists",
            description="Check if a file exists on SFTP server",
            inputSchema={
                "type": "object",
                "properties": {
                    "connection_name": {
                        "type": "string",
                        "description": "Name of the SFTP connection"
                    },
                    "remote_path": {
                        "type": "string",
                        "description": "Remote file path"
                    }
                },
                "required": ["connection_name", "remote_path"]
            }
        ),
        Tool(
            name="validate_file",
            description="Validate file naming convention and metadata",
            inputSchema={
                "type": "object",
                "properties": {
                    "connection_name": {
                        "type": "string",
                        "description": "Name of the SFTP connection"
                    },
                    "remote_path": {
                        "type": "string",
                        "description": "Remote file path"
                    },
                    "partner": {
                        "type": "string",
                        "description": "Banking partner code (PARTNER_A, PARTNER_B, GENERIC)",
                        "default": "GENERIC"
                    }
                },
                "required": ["connection_name", "remote_path"]
            }
        ),
        Tool(
            name="send_slack_alert",
            description="Send alert message to Slack channel",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Alert message to send"
                    },
                    "channel": {
                        "type": "string",
                        "description": "Slack channel ID or name"
                    },
                    "severity": {
                        "type": "string",
                        "description": "Alert severity (info, warning, error)",
                        "enum": ["info", "warning", "error"],
                        "default": "info"
                    }
                },
                "required": ["message", "channel"]
            }
        ),
        Tool(
            name="monitor_files",
            description="Monitor SFTP directory for expected files and validate them",
            inputSchema={
                "type": "object",
                "properties": {
                    "connection_name": {
                        "type": "string",
                        "description": "Name of the SFTP connection"
                    },
                    "remote_path": {
                        "type": "string",
                        "description": "Remote directory path to monitor"
                    },
                    "partner": {
                        "type": "string",
                        "description": "Banking partner code (PARTNER_A, PARTNER_B, GENERIC)",
                        "default": "GENERIC"
                    },
                    "expected_patterns": {
                        "type": "array",
                        "description": "List of expected file patterns",
                        "items": {"type": "string"}
                    }
                },
                "required": ["connection_name", "remote_path", "partner"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""

    try:
        if name == "connect_sftp":
            return await connect_sftp_tool(arguments)
        elif name == "list_files":
            return await list_files_tool(arguments)
        elif name == "check_file_exists":
            return await check_file_exists_tool(arguments)
        elif name == "validate_file":
            return await validate_file_tool(arguments)
        elif name == "send_slack_alert":
            return await send_slack_alert_tool(arguments)
        elif name == "monitor_files":
            return await monitor_files_tool(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        logger.error(f"Error executing tool {name}: {str(e)}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def connect_sftp_tool(args: dict) -> list[TextContent]:
    """Connect to SFTP server"""
    connection_name = args["connection_name"]

    client = SFTPClient(
        host=args["host"],
        port=args.get("port", 22),
        username=args["username"],
        password=args.get("password"),
        private_key_path=args.get("private_key_path")
    )

    if client.connect():
        active_connections[connection_name] = client
        result = {
            "success": True,
            "message": f"Connected to {args['host']} as {connection_name}",
            "connection_name": connection_name
        }
    else:
        result = {
            "success": False,
            "message": f"Failed to connect to {args['host']}",
            "connection_name": connection_name
        }

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def list_files_tool(args: dict) -> list[TextContent]:
    """List files in SFTP directory"""
    connection_name = args["connection_name"]

    if connection_name not in active_connections:
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": f"No active connection named '{connection_name}'"
        }))]

    client = active_connections[connection_name]
    remote_path = args.get("remote_path", ".")

    files = client.list_files(remote_path)

    result = {
        "success": True,
        "path": remote_path,
        "file_count": len(files),
        "files": files
    }

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def check_file_exists_tool(args: dict) -> list[TextContent]:
    """Check if file exists on SFTP server"""
    connection_name = args["connection_name"]

    if connection_name not in active_connections:
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": f"No active connection named '{connection_name}'"
        }))]

    client = active_connections[connection_name]
    remote_path = args["remote_path"]

    exists = client.file_exists(remote_path)
    metadata = client.get_file_metadata(remote_path) if exists else None

    result = {
        "success": True,
        "path": remote_path,
        "exists": exists,
        "metadata": metadata
    }

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def validate_file_tool(args: dict) -> list[TextContent]:
    """Validate file on SFTP server"""
    connection_name = args["connection_name"]

    if connection_name not in active_connections:
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": f"No active connection named '{connection_name}'"
        }))]

    client = active_connections[connection_name]
    remote_path = args["remote_path"]
    partner = args.get("partner", "GENERIC")

    # Get file metadata
    metadata = client.get_file_metadata(remote_path)

    if not metadata:
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": f"File not found: {remote_path}"
        }))]

    # Extract filename from path
    filename = os.path.basename(remote_path)

    # Validate file
    validator = FileValidator(partner)
    validation_result = validator.validate_all(
        filename=filename,
        file_size=metadata['size'],
        file_mtime=metadata['mtime']
    )

    result = {
        "success": True,
        "path": remote_path,
        "validation": validation_result
    }

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def send_slack_alert_tool(args: dict) -> list[TextContent]:
    """Send alert to Slack"""
    if not SLACK_AVAILABLE:
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": "Slack SDK not available. Install with: pip install slack-sdk"
        }))]

    slack_token = os.getenv("SLACK_BOT_TOKEN")
    if not slack_token:
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": "SLACK_BOT_TOKEN environment variable not set"
        }))]

    message = args["message"]
    channel = args["channel"]
    severity = args.get("severity", "info")

    # Add emoji based on severity
    emoji_map = {
        "info": ":information_source:",
        "warning": ":warning:",
        "error": ":rotating_light:"
    }
    emoji = emoji_map.get(severity, ":bell:")

    try:
        client = WebClient(token=slack_token)
        response = client.chat_postMessage(
            channel=channel,
            text=f"{emoji} {message}",
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{emoji} *{severity.upper()}*\n{message}"
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"_Sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_"
                        }
                    ]
                }
            ]
        )

        result = {
            "success": True,
            "message": "Alert sent to Slack",
            "channel": channel,
            "severity": severity
        }
    except SlackApiError as e:
        result = {
            "success": False,
            "error": f"Slack API error: {str(e)}"
        }

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def monitor_files_tool(args: dict) -> list[TextContent]:
    """Monitor SFTP directory for files and validate them"""
    connection_name = args["connection_name"]

    if connection_name not in active_connections:
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": f"No active connection named '{connection_name}'"
        }))]

    client = active_connections[connection_name]
    remote_path = args["remote_path"]
    partner = args.get("partner", "GENERIC")

    # List files in directory
    files = client.list_files(remote_path)

    # Filter only files (not directories)
    files = [f for f in files if not f['is_dir']]

    # Validate each file
    validator = FileValidator(partner)
    validated_files = []

    for file_info in files:
        validation_result = validator.validate_all(
            filename=file_info['filename'],
            file_size=file_info['size'],
            file_mtime=file_info['mtime']
        )

        validated_files.append({
            "file": file_info['filename'],
            "size": file_info['size'],
            "modified": file_info['modified_date'],
            "valid": validation_result['valid'],
            "errors": validation_result['errors'],
            "warnings": validation_result['warnings']
        })

    # Summary
    total_files = len(validated_files)
    valid_files = sum(1 for f in validated_files if f['valid'])
    invalid_files = total_files - valid_files

    result = {
        "success": True,
        "path": remote_path,
        "partner": partner,
        "summary": {
            "total_files": total_files,
            "valid_files": valid_files,
            "invalid_files": invalid_files
        },
        "files": validated_files
    }

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


if __name__ == "__main__":
    import asyncio
    import mcp

    async def main():
        """Run the MCP server"""
        from mcp.server.stdio import stdio_server

        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )

    asyncio.run(main())
