from infrahub_sdk import InfrahubClient
import logging

async def run(
    client: InfrahubClient,
    log: logging.Logger,
    branch: str
):
    # tags = await client.all(kind="BuiltinTag")
    # print(tags)

    # tag = await client.create(kind="BuiltinTag", name="purple")
    # await tag.save(allow_upsert=True)
    # print(tag.id)

    batch = await client.create_batch()

    for i in range(10):
        tag = await client.create(kind="BuiltinTag",
                name=f"blue-0{i}")
        batch.add(task=tag.save, allow_upsert=True, node=tag)

        async for node, result in batch.execute():
            print(node.name.value)