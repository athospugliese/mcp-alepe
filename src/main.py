"""
Ponto de entrada principal para o servidor MCP da ALEPE.
"""
import os
import asyncio
import json
from fastmcp import FastMCP
from src.alepe_tools import register_alepe_tools

mcp = FastMCP("MCP ALEPE Server")
register_alepe_tools(mcp)

def main():
    # Check if running on Railway (or similar platform)
    if os.environ.get("PORT"):
        # For Railway deployment, we need to create a simple HTTP server
        # that can handle MCP requests over HTTP
        from http.server import HTTPServer, BaseHTTPRequestHandler
        import threading
        
        class MCPHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b'MCP ALEPE Server is running!')
                elif self.path == '/health':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "healthy"}).encode())
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def do_POST(self):
                # Handle MCP requests over HTTP
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                try:
                    # This would need proper MCP protocol handling
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "MCP over HTTP not implemented yet"}).encode())
                except Exception as e:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": str(e)}).encode())
        
        port = int(os.environ.get("PORT", 8000))
        server = HTTPServer(('0.0.0.0', port), MCPHandler)
        print(f"Starting HTTP server on port {port}")
        server.serve_forever()
    else:
        # Standard MCP server over stdio
        mcp.run()

if __name__ == "__main__":
    main()