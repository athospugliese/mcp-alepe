"""
Ponto de entrada principal para o servidor MCP da ALEPE.
"""
from fastmcp import FastMCP
from src.alepe_tools import register_alepe_tools

mcp = FastMCP("MCP ALEPE Server")
register_alepe_tools(mcp)

def main():
    mcp.run()

if __name__ == "__main__":
    main()