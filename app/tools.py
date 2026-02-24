class Tools():
    tools=[
    {
        "type": "function",
        "function": {
            "name": "Read",
            "description": "Read and return the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path of the file to read"
                    }
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function", 
        "function": {
            "name": "Write",
            "description": "Write content into a file",
            "parameters": {
                "type": "object",
                "required": ["file_path", "content"],
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path of the file to write to"
                    },    
                    "content": {
                        "type": "string",
                        "description": "The content to write to the file"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "Bash",
            "description": "Execute a shell command",
            "parameters": {
                "type": "object",
                "required": ["command"],
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command to execute"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "Confusion",
            "description": "Set this flag if you are confused",
            "parameters": {
                "type": "object",
                "properties": {
                    "confused": {
                        "type": "boolean",
                        "description": "True if confused, False if not confused"
                    }
                },
                "required": ["confused"]
            }
        }
    }
    ]

tools = Tools()
