
import asyncio, time

@commands.slash_command(name="harvest", description="Harvests data from a guild.")
async def harvest(self, ctx):
    await ctx.defer()

    guild = ctx.guild
    data_list = {}
    start_time = time.time()
    count = 0

    async def harvest_channel(channel, count):
        # Iterate through all messages in the channel
        async for message in channel.history(limit=None):
            data_list[channel.name].append([
                message.id, message.content, message.author.id, message.created_at,
                message.reference.message_id if message.reference else None,
                str([mention.id for mention in message.mentions]) if message.mentions != [] else None
            ])
            count += 1
            if count % 100 == 0:
                print(count)

    async def middle(channel, count):

        # run the harvest_channel function in a new thread
        await harvest_channel(channel, count)

    thread_list = []

    # Iterate through all channels in the guild
    for channel in guild.channels:

        # check if channel is a text channel
        if not isinstance(channel, discord.TextChannel):
            continue

        # Iterate through all messages in the channel
        data_list[channel.name] = []
        channel = self.client.get_channel(channel.id)
        log.info(f"Harvesting channel {channel.name}...")

        from multiprocessing import Process

        process = Process(target=asyncio.run, args=(middle(channel, count),))
        thread_list.append(process)


    # wait for all threads to finish

    for process in thread_list:
        process.start()

    for process in thread_list:
        process.join()

    # Add the data to the database
    for channel in data_list:
        print(channel)
        self.manager.add_bulk_data(guild.id, data_list[channel])

    await ctx.followup.send("Harvested data from the guild.")
    log.info(f"Harvested data from guild {guild.id} in {time.time() - start_time} seconds.")