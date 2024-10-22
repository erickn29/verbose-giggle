import aiohttp


async def get_evaluation_request(url: str, data: dict):
    async with (
        aiohttp.ClientSession() as session,
        session.post(
            url, json=data, headers={"Content-Type": "application/json"}
        ) as response,
    ):
        try:
            return await response.json()
        except aiohttp.ClientError:
            return None
