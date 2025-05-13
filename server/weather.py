from typing import Any
from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("weather")

NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"


async def make_weather_https_request(url: str) -> dict[str, Any] | None:
    """Make a request to NWS API with error handling properly."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
        

def format_weather_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    properties = feature["properties"]
    return f"""
        Event: {properties.get('event', 'Unknown')}
        Area: {properties.get('areaDesc', 'Unknown')}
        Severity: {properties.get('severity', 'Unknown')}
        Description: {properties.get('description', 'No description available')}
        Instructions: {properties.get('instruction', 'No specific instructions provided')}
        """
        
@mcp.tool()
async def get_weather_alerts(state:str) ->str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/activate/area/{state}"
    data = await make_weather_https_request(url)
    
    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."
    
    weather_alerts = [format_weather_alert(feature) for feature in data["features"]]
    return "\n---\n".join(weather_alerts)