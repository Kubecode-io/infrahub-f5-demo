from infrahub_sdk import InfrahubClient
import logging

# infrahubctl run scripts/test.py --branch=F5_DEMO

async def run(
    client: InfrahubClient,
    log: logging.Logger,
    branch: str
):

    ltm_ha_group = await client.get(kind="LoadbalancerLTMHAGroup", name__value="ukdc1-n-slb0102")

    pool_args = {
        "object_name": "BLUE-DGA-INT-NAP-V-1C-BIE_7777_POOL",
        "partition": "Common",
    }

    pool = await client.create(kind="F5networksPool", **pool_args)
    await pool.save(allow_upsert=True)
    print("POOL:", pool.id)

    vip_args = {
        "object_name": "BLUE-DGA--INT-NAP-V-1C-BIE_80_VS",
        "partition": "Common",
        "destination_partition": "Common",
        "destination_address": "10.130.13.166",
        "destination_service_port": 80,
        "source_address": "0.0.0.0/0",
        "pool": pool,
        "ltm_ha_group": ltm_ha_group
    }

    # vips = await client.all(kind="F5networksVIP")
    # print(vips)

    vip = await client.create(kind="F5networksVIP", **vip_args)
    await vip.save(allow_upsert=True)
    print("VIP:", vip.id)

    vips = [vip]
    rule_args = {
        "object_name": "GOLDEN",
        "partition": "Common",
        "script": "Meh",
        "vip": vips
    }

    rule = await client.create(kind="F5networksRule", **rule_args)
    await rule.save(allow_upsert=True)
    print("RULE:", rule.id)
