import aiohttp


async def get_evaluation(url: str, data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url, json=data, headers={"Content-Type": "application/json"}
        ) as response:
            try:
                print("send request to model")
                return await response.json()
            except aiohttp.ClientError:
                return None
