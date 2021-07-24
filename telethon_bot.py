import os
from dotenv import load_dotenv
from telethon.sync import TelegramClient, events, utils, Button
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors import UserAlreadyParticipantError

load_dotenv()

API_ID = os.getenv('API_ID1')
API_HASH = os.getenv('API_HASH1')
USER_NAME = os.getenv('USER_NAME1') #login as a bot
# PHONE = os.getenv('PHONE1') #login as a user

welcome_str = "**Welcome to Pegaswap!**\n\nThe next-gen Decentralized Exchange, Staking, and Farming Protocol on BSC.\n\nPegaSwap is a DeFi protocol running on the Binance Smart Chain (BSC). It allows you to swap between tokens issued on BSC, and earn rewards for providing liquidity to these decentralized markets, with lots of other features that let you earn and win tokens. PegaSwap was built by Pegasus Finance. We have a dedicated team of experienced Pegasus Finance, who have been in the crypto space for years. PGS is the native currency of our platform. Stake, pool, and earn $PGS all on PegaSwap.\nPegaSwap works as a decentralized exchange (DEX) that adopts the automated market maker (AMM) model. Similar to PancakeSwap, BakerySwap, and other protocols, it allows users to earn tokens by providing liquidity."
what_str = "PegaSwap is a fairly new decentralized exchange (DEX) that’s been created on the Binance Smart Chain (BSC). The automated market maker (AMM) offers users a number of innovative ways to create income streams from their cryptocurrencies.\nDeFi, or Decentralized Finance, provides peer-to-peer alternatives to traditional financial services and institutions. The PegaSwap platform brings DeFi and higher APYs (Annual Percentage Yields) to members by eliminating intermediaries, central oversight, and removing technical knowledge, making financial markets more accessible to underserved communities. \nPGS is a platform that empowers you to be in control of your finances by creating cash flow and harnessing the potentials of Decentralized Finance."
investment_str = "An angel investor (also known as a private investor, seed investor, or angel investor) is a high net worth individual who provides financial support to a startup. from us, from which you will receive profits from participating in the project's activities through smart contracts on the available platform:\n\nInvestors have the right to participate in a smart contract to receive 0.01% of the transaction fees collected from the swap platform, provided that they put in a lock of 60% of the PGS obtained from participating in the Investor Angel program. Get the right to administer the protocol and vote (Government & Voting). Divided income fee quarterly."
howto_trade_str = "**How to trade on PegaSwap**: https://docs.pegaswap.com/swap/How-to-Trade-on-PegaSwap"
howto_buy_str = "**How to buy PGS**: \n\n1. You go to: https://pegaswap.com/#/sale \n\n2. Unlock your Binance Smart Chain Wallet. \n\n3. Deposit BNB. \n\n4. Total PGS Received. \n\n5. You can earn Reward by partner: https://pegaswap.com/#/sale?address=0x353Bd5864e1b0Efad21B90275164ABDfEA6e4605 \n\n6. You can earn Cash back: https://pegaswap.com/#/sale?address=0x353Bd5864e1b0Efad21B90275164ABDfEA6e4605"
farm_str = "Yield farm is comming soon!"

keyboard = [
    [  
        Button.inline("Welcome to Pegaswap!", b"welcome"), 
        Button.inline("What is PegaSwap?", b"what")
    ],
    [
        Button.inline("Investment", b"investment"), 
        Button.inline("How to trade on PegaSwap?", b"howto_trade")
    ],
    [
        Button.inline("How can buy PGS?", b"howto_buy"),
        Button.inline("Farm (comming soon)", b"farm")
    ]
]

with TelegramClient(USER_NAME, API_ID, API_HASH) as bot:
    print("Telegram bot start")

    @bot.on(events.NewMessage)
    async def handler(event):
        print(event.message.peer_id, event.message.message)

    # @bot.on(events.NewMessage(pattern="(?i).* hi|hello"))
    # async def handler(event):
    #     sender = await event.get_sender()
    #     await event.respond(f"Hello, {sender.first_name} ✌️")

    @bot.on(events.callbackquery.CallbackQuery(data = b"welcome"))
    async def handler(event):
        print("welcome")
        await event.respond(welcome_str, buttons = keyboard)

    @bot.on(events.callbackquery.CallbackQuery(data = b"what"))
    async def handler(event):
        print("what")
        await event.respond(what_str, buttons = keyboard)

    @bot.on(events.callbackquery.CallbackQuery(data = b"investment"))
    async def handler(event):
        print("investment")
        await event.respond(investment_str, buttons = keyboard)

    @bot.on(events.callbackquery.CallbackQuery(data = b"howto_trade"))
    async def handler(event):
        print("howto_trade")
        await event.respond(howto_trade_str, buttons = keyboard)

    @bot.on(events.callbackquery.CallbackQuery(data = b"howto_buy"))
    async def handler(event):
        print("howto_buy")
        await event.respond(howto_buy_str, buttons = keyboard)

    @bot.on(events.callbackquery.CallbackQuery(data = b"farm"))
    async def handler(event):
        print("farm")
        await event.respond(farm_str, buttons = keyboard)

    @bot.on(events.NewMessage(pattern="/information|/start"))
    async def handler(event):
        await event.respond("Which's information you want to know?", buttons = keyboard)

    bot.run_until_disconnected()
